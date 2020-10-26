# -*- coding: utf-8 -*-

from odoo import models, api,fields, _
from odoo.tools import ustr


class ResPartner(models.Model):
    _inherit = "res.partner"

    employee_id = fields.Many2one('hr.employee', string="employee")


    @api.model
    def create(self, values):
        res = super(ResPartner, self).create(values)
        if not res.employee_id and self.env.user.id != 1:
            job_name = ''
            user_id = self.env['res.users']
            if res.consultant or res.is_business_manager:
                if res.consultant:
                    job_name = 'Consultant'
                    user_id = self.env['res.users'].search([('login', '=', res.email)])
                if res.is_business_manager:
                    job_name = 'MANAGER'
                    user_id = self.env['res.users'].search([('login', '=', res.email)])
                if not user_id:
                    self.env.user.company_id.create_consultant_public_user()
                    user_id = user = self.env['res.users'].search([('login', '=', res.email)])
                job_id = self.env['hr.job'].search([('name', '=', job_name)])
                data = {'company_id': self.env.user.company_id.id,
                            'lastname': res.name.split(' ')[0] or ' ',
                            'firstname': res.name.split(' ')[1] or ' ',
                            'job_id': job_id.id,
                            'active': res.active,
                            'work_email': res.email,
                            'mobile_phone': res.mobile,
                            'work_phone': res.phone,
                            'user_id': user_id.id or False}
                employee = self.env['hr.employee'].create(data)
                res.employee_id = employee.id
        return res
        
    
    @api.multi
    def write(self, values):
        for record in self:
            res = super(ResPartner, self).write(values)
            if not record.employee_id and self.env.user.id != 1:
                job_name = ''
                user_id = self.env['res.users']
                if record.consultant or record.is_business_manager:
                    if record.consultant:
                        job_name = 'Consultant'
                        user_id = self.env['res.users'].search([('login', '=', record.email)])
                    if record.is_business_manager:
                        job_name = 'MANAGER'
                        user_id = self.env['res.users'].search([('login', '=', record.email)])
                    if not user_id:
                        self.env.user.company_id.create_consultant_public_user()
                        user_id = self.env['res.users'].search([('login', '=', record.email)])
                    job_id = self.env['hr.job'].search([('name', '=', job_name)])
                    data = {'company_id': self.env.user.company_id.id,
                                'lastname': record.name.split(' ')[0] or ' ',
                                'firstname': record.name.split(' ')[1] or ' ',
                                'job_id': job_id.id,
                                'active': record.active,
                                'work_email': record.email,
                                'mobile_phone': record.mobile,
                                'work_phone': record.phone,
                                'user_id': user_id.id or False}
                    employee = self.env['hr.employee'].create(data)
                    record.employee_id = employee.id
            return res
    
    @api.model
    def simus_create_subcontractor(self, cr, lines, company_simus_codes, users_simus_code):
        result = {'nb_lines': len(lines), 'nb_partners_created': 0, 'nb_partners_updated': 0,
                  'partners_error': "", 'partners_created': ""}
        for line in lines:
            try:
                company = company_simus_codes.get(line[1])
                if company:
                    simus_code = line[5]
                    company_id = company['id']
                    name = line[8] + " " + line[7]
                    email = line[20].split(',')[0].strip() if '@' in line[20] else ''
                    data = {'company_id': company_id,
                            'lastname': line[7],
                            'firstname': line[8],
                            'simus_code': simus_code,
                            'email': email,
                            'user_id': users_simus_code.get(line[13]),
                            'tz': 'Europe/Paris'}
                    partners = company['partners_simus_code']
                    for partner in partners.filtered(lambda part: part.name == line[4]
                                                     and part.simus_code != simus_code
                                                     ).sorted(lambda part: part.id):
                        data['parent_id'] = partner.id
                        break
                    partner_id = company['partner_simus_codes'].get(simus_code)
                    if partner_id:
                        partner = self.with_context(active_test=False).browse(partner_id)
                        data['is_modify_name'] = not partner.is_modify_name
                        partner.write(data)
                        result['nb_partners_updated'] += 1
                    else:
                        partners = company['partners_no_simus_code']
                        partners = partners.filtered(lambda part: part.email == email and not part.simus_code)
                        if not partners:
                            partner = self.create(data)
                            partner_id = partner.id
                            val = '<br></br><div>' + "id: %s" % partner_id + " name: " + ustr(name) + " simus_code: %s company_id: %s" % (simus_code, company_id) + '</div>'
                            result['partners_created'] += val
                            result['nb_partners_created'] += 1
                            company['partner_simus_codes'][simus_code] = partner_id
                            company['partners_simus_code'] |= partner
                            company['partners_no_simus_code'] -= partner
                        else:
                            partners.write(data)
                        result['nb_partners_updated'] += len(partners)
                else:
                    result['partners_error'] += '<br></br><div>' + "Partner error no company found: " + ustr(line) + '</div>'
            except Exception as e:
                val = '<br></br><div>' + "Partners error:" + ustr(line) + "</div><br></br><div>" + "error: " + ustr(e) + "</div>"
                result['partners_error'] += val
                continue
        try:
            if lines:
                cr.commit()
        except Exception as e:
            return {'commit_error': e}
        return result
