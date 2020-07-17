# -*- coding: utf-8 -*-

from odoo import models, api, _
from datetime import datetime
from os.path import exists
from odoo.tools import ustr
import csv


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.multi
    def write(self, vals):
        for company in self:
            if company.simus_code and vals.get('simus_code'):
                vals.pop('simus_code')
        return super(ResCompany, self).write(vals)

    @api.model
    def simus_send_email(self, subject, body, user_admin_id):
        mail_obj = self.env['mail.mail'].sudo(user_admin_id)
        mailing_list = self.env.ref('aaa_simus.simus_mailing_list').sudo().value
        mail_sender = self.env.ref('aaa_simus.simus_mail_sender_o365').sudo().value
        mail_server = self.env['ir.mail_server'].search([('smtp_user', '=', mail_sender)], limit=1)
        mail_server_id = mail_server.id
        self.env['mail.mail'].sudo(user_admin_id).create({'mail_server_id': mail_server_id,
                                                          'email_from': mail_sender,
                                                          'reply_to': mail_sender,
                                                          'email_to': mailing_list,
                                                          'subject': subject,
                                                          'body_html': body})

    @api.model
    def simus_create_company(self, simus_code, name, currency_id, parent_id, company_simus_codes,
                             company_id_simus_codes, admin_users, partner_obj):
        company = self.create({'simus_code': simus_code,
                               'name': name,
                               'currency_id': currency_id,
                               'parent_id': parent_id})
        company.partner_id.simus_code = simus_code
        company_id = company.id
        admin_users.write({'company_ids': [(4, company_id)]})
        company_id_simus_codes[company_id] = simus_code
        company_simus_codes[simus_code] = {'id': company_id, 'partner_simus_codes': {},
                                           'employee_simus_codes': {}, 'job_names': {},
                                           'partners_simus_code': partner_obj,
                                           'partners_no_simus_code': partner_obj}
        return company_id, name

    @api.model
    def simus_import_resources(self):
        ftp = self.env['res.ftp'].search([])
        path = ftp.file_name
        if exists(path):
            user_admin = self.env.ref('base.user_admin')
            user_admin_id = user_admin.id
            admin_users = self.env.ref('base.user_root') + user_admin
            user_obj = self.env['res.users']
            partner_obj = self.env['res.partner']
            employee_obj = self.env['hr.employee']
            job_obj = self.env['hr.job']
            hr_contract_obj = self.env['hr.contract']
            currency_id = self.env.ref('base.EUR').id
            parent_company_id = self.env.ref('base.main_company').id
            cr = self._cr
            company_simus_codes = {}
            company_id_simus_codes = {}
            for company in self.search_read([], ['simus_code']):
                company_id = company['id']
                company_simus_codes[company['simus_code']] = {'id': company_id, 'partner_simus_codes': {},
                                                              'employee_simus_codes': {}, 'job_names': {},
                                                              'partners_simus_code': partner_obj,
                                                              'partners_no_simus_code': partner_obj}
                company_id_simus_codes[company_id] = company['simus_code']
            lines = {}
            company_ids = []
            company_errors = new_companies = ""
            with open(path, 'r') as resources_file:
                resources_reader = csv.reader(resources_file, delimiter=',', quotechar='"')
                for line in resources_reader:
                    if line[1] == 'Identifiant cabinet':
                        #pass
                        #next(resources_reader)
                        break
                for line in resources_reader:
                    if line and line[1] not in ['INP', 'INS']:
                        simus_code = line[1]
                        if not line[2] in lines:
                            lines[line[2]] = []
                        lines[line[2]].append(line)
                        if simus_code:
                            try:
                                if simus_code not in company_simus_codes:
                                        company_id, name = self.simus_create_company(simus_code, line[0], currency_id, parent_company_id,
                                                                                     company_simus_codes, company_id_simus_codes,
                                                                                     admin_users, partner_obj)
                                        company_ids += [company_id]
                                        val = '<br></br><div>' + "id: " + ustr(company_id) + " name: " + ustr(name) + " simus_code: %s" % simus_code + '</div>'
                                        new_companies += val
                                else:
                                    company_id = company_simus_codes[simus_code]['id']
                                    if company_id not in company_ids:
                                        company_ids += [company_id]
                            except Exception as e:
                                val = '<br></br><div>' + "Company errors :" + ustr(line) + "</div><br></br><div>" + "error: " + ustr(e) + '</div>'
                                company_errors += val
                                continue
                        else:
                            company_errors += '<br></br><div>' + "No simus code: " + ustr(line) + '</div>'
            lines_business_manager = lines.get('BM')
            lines_employee = lines.get('Salarié')
            lines_detachment = lines.get('Détachement')
            lines_subcontractor = lines.get('Externe')
            for job in job_obj.search_read([], ['name', 'company_id']):
                company_id = job['company_id'] and job['company_id'][0]
                if company_id in company_ids:
                    company_simus_codes[company_id_simus_codes[company_id]
                                        ]['job_names'][job['name']] = job['id']
            for partner in partner_obj.with_context(active_test=False).search_read([], ['simus_code', 'company_id']):
                company_id = partner['company_id'] and partner['company_id'][0]
                if company_id in company_ids:
                    company = company_simus_codes[company_id_simus_codes[company_id]]
                    if partner['simus_code']:
                        company['partner_simus_codes'][partner['simus_code']] = partner['id']
                        company['partners_simus_code'] |= partner_obj.with_context(active_test=False).browse(partner['id'])
                    else:
                        company['partners_no_simus_code'] |= partner_obj.with_context(active_test=False).browse(partner['id'])
            for employee in employee_obj.with_context(active_test=False).search_read([('simus_code', '!=', '')],
                                                                                     ['company_id', 'simus_code']):
                company_id = employee['company_id'] and employee['company_id'][0]
                if company_id:
                    employee_id = employee['id']
                    company = company_simus_codes[company_id_simus_codes[company_id]]
                    employee_simus_code = employee['simus_code']
                    if employee_simus_code:
                        company['employee_simus_codes'][employee_simus_code] = employee_id
            users_login = {}
            users_simus_code = {}
            for user in user_obj.with_context(active_test=False).search_read([], ['login', 'simus_code']):
                simus_code = user['simus_code']
                user_id = user['id']
                users_login[user['login']] = user_id
                if simus_code:
                    users_simus_code[simus_code] = user_id
            if lines_business_manager:
                result, users_simus_code, users_login = user_obj.simus_business_manager(cr, lines_business_manager, company_simus_codes,
                                                                                    users_login, users_simus_code, employee_obj)
            if lines_employee:
                result = employee_obj.simus_employee(cr, lines_employee, company_simus_codes, users_login,
                                                 job_obj, hr_contract_obj)
            if lines_detachment:
                result = employee_obj.simus_employee(cr, lines_detachment, company_simus_codes, users_login,
                                                 job_obj, hr_contract_obj)
            if lines_subcontractor:
                result = partner_obj.simus_create_subcontractor(cr, lines_subcontractor, company_simus_codes,
                                                            users_simus_code)
            
            self.create_consultant_public_user()

    @api.model
    def get_contact_name(self, partners, contact_name):
        contact_name = contact_name.lower()
        for contact in partners.filtered(lambda part: contact_name in part.name.lower()):
            return contact.id
        return False

    @api.model
    def simus_import_projects(self):
        ftp = self.env['res.ftp'].search([])
        path = ftp.file_name_sec
        if exists(path):
            user_obj = self.env['res.users']
            partner_obj = self.env['res.partner']
            project_obj = self.env['project.project']
            task_obj = self.env['project.task']
            lines = []
            with open(path, 'r') as projects_file:
                projects_reader = csv.reader(projects_file, delimiter=',', quotechar='"')
                date_end = self.env.ref('aaa_simus.simus_project_date_min').sudo().value
                for line in projects_reader:
                    if line[1] == 'Identifiant cabinet':
                        pass
                    else:
                        date_end_project = line[5]
                        if line[0] and date_end_project and datetime.strptime(date_end_project, '%Y-%m-%d') >= datetime.strptime(date_end, '%Y-%m-%d'):
                            lines.append(line)
                        for line in lines:
                            company = self.env['res.company'].search([('simus_code', '=', line[1])])
                            if company and not line[1] in ['INP', 'INS']:
                                simus_code = line[9]
                                company_id = company.id
                                name = line[8]
                                partner_data = {'simus_code': simus_code,
                                                'company_id': company_id,
                                                'lastname': name,
                                                'firstname': '',
                                                'customer': True,
                                                'is_company': True}
                                customer = partner_obj.search([('simus_code', '=',simus_code), ('company_id', '=', company_id)])
                                if customer:
                                    customer.write(partner_data)
                                else:
                                    customer = partner_obj.create(partner_data)
                                customer_id = customer[0].id
                                user_id = self.env['res.users'].search([('simus_code', '=',line[15])])
                                project_code = line[2]
                                name = line[6]
                                project_data = {'simus_code': project_code,
                                                'partner_id': customer_id,
                                                'company_id': company_id,
                                                'user_id': user_id,
                                                'name': name,
                                                'description': line[7]}
                                project = project_obj.search([('simus_code', '=', project_code)])
                                if project:
                                    project.write(project_data)
                                else:
                                    project = project_obj.create(project_data)
                                project_id = project.id
                                task_code = project_code + " - " + line[14]
                                active = True
                                date_deadline = line[19]
                                date_now = datetime.now()
                                min_date = self.env.ref('aaa_simus.simus_project_date_min').value
                                if date_deadline and datetime.strptime(date_deadline, '%Y-%m-%d') < date_now and datetime.strptime(date_deadline, '%Y-%m-%d') >= datetime.strptime(min_date, '%Y-%m-%d'):
                                    active = False
                                if date_deadline and datetime.strptime(date_deadline, '%Y-%m-%d').year == 0 and datetime.strptime(date_deadline, '%Y-%m-%d').month == 0 and datetime.strptime(date_deadline, '%Y-%m-%d').day == 0:
                                    active= True
                                contact_id = customer_id
                                contact_client = line[27] or line[28] or False
                                if contact_client:
                                    partners = partner_obj.with_context(active_test=False).browse(customer_id).child_ids
                                    if partners:
                                        res = self.get_contact_name(partners, contact_client)
                                        if res:
                                            contact_id = res
                                name = line[6]
                                data_task = {'simus_code': task_code,
                                            'partner_id': contact_id,
                                            'company_id': company_id,
                                            'project_id': project_id,
                                            'user_id': user_id,
                                            'code_type': 'mission',
                                            'date_start': line[18],
                                            'date_deadline': date_deadline,
                                            'active': active,
                                            'name': name,
                                            'description': line[7]}
                                task= task_obj.search([('simus_code', '=', task_code)])
                                if task:
                                    task.write(data_task)
                                else:
                                    task_obj.create(data_task)
                                    
                                    
    @api.model
    def create_consultant_public_user(self):
        consultants = self.env['res.partner'].search([('consultant', '=', True), ('user_ids', '=', False)])
        user_obj = self.env['res.users']
        if consultants:
            for consultant in consultants:
                default_login = consultant.lastname + '@' + consultant.firstname + '.com'
                user_vals = {'company_id': consultant.company_id.id,
                                 'lastname': consultant.lastname,
                                 'firstname': consultant.firstname,
                                 'mobile': consultant.mobile,
                                 'phone': consultant.phone,
                                 'active': consultant.active,
                                 'tz': 'Europe/Paris',
                                 'login': consultant.email or default_login,
                                 'level': 1,
                                 'partner_id': consultant.id,
                                 'company_ids': [(6, 0, [consultant.company_id.id])]}
                user = user_obj.search([('login', '=', consultant.email)])
                default_user = user_obj.search([('login', '=', default_login)])
                if not default_user and not user:
                    user = user_obj.create(user_vals)
                    user.write({'groups_id':[(5,0,0)]})                
                    public_group_id = self.env.ref('base.group_public').sudo().id
                    user.write({'groups_id': [(4, public_group_id)]})
