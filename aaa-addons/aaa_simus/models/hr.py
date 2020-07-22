# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from datetime import datetime
from odoo.tools import ustr
import ftplib as ftp
import pysftp


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    #child_ids_text = fields.Text(string="child child ids")

    @api.model
    def simus_create_job(self, job_name, company_id, company, job_obj):
        job = job_obj.create({'name': job_name, 'company_id': company_id})
        job_id = job.id
        company['job_names'][job_name] = job_id
        return job_id

    @api.model
    def simus_get_parent_id(self, data, parent_id, employee_id, result, line, company_id):
        if parent_id:
            if parent_id == employee_id:
                data['parent_id'] = False
            else:
                data['parent_id'] = parent_id
        else:
            result['employees_error'] += '<br></br><div>' + "Employee error no bm found for company_id %s : %s" % (company_id, line) + "</div>"
        return parent_id

    @api.model
    def simus_employee(self, cr, lines, company_simus_codes, users_login, job_obj, hr_contract_obj):
        result = {'nb_lines': len(lines), 'nb_employees_created': 0, 'nb_employees_updated': 0,
                  'employees_error': "", 'employees_created': "", 'nb_contracts_created': 0,
                  'nb_contracts_updated': 0, 'contracts_created': ""}
        for line in lines:
            try:
                company = company_simus_codes.get(line[1])
                if company:
                    simus_code = line[5]
                    company_id = company['id']
                    work_email = line[20].split(',')[0].strip() if '@' in line[20] else ''
                    job_name = line[30]
                    active = True
                    date_end = None
                    if line[16] and line[16] != '0000-00-00':
                        active = False
                        date_end = datetime.strptime(line[16], '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                    parent_id = company['employee_simus_codes'].get(line[13])
                    user_id = users_login.get(work_email)
                    name = line[8] + " " + line[7]
                    data = {'company_id': company_id,
                            'lastname': line[7],
                            'firstname': line[8],
                            'simus_code': simus_code,
                            'job_id': company['job_names'].get(job_name) or self.simus_create_job(job_name, company_id,
                                                                                                  company, job_obj),
                            'active': active,
                            'leaves_previous_year': float(line[26]) if line[26] else 0,
                            'leaves_current_year': float(line[27]) if line[27] else 0,
                            'leaves_employer': float(line[28] if line[28] else 0),
                            'leaves_employee': float(line[29] if line[29] else 0),
                            'work_email': work_email,
                            'mobile_phone': line[19],
                            'work_phone': line[18],
                            'user_id': user_id}
                    employee_id = company['employee_simus_codes'].get(simus_code)
                    if employee_id:
                        self.simus_get_parent_id(data, parent_id, employee_id, result, line, company_id)
                        employee = self.with_context(active_test=False).browse(employee_id)
                        data['is_modify_name'] = not employee.is_modify_name
                        employee.write(data)
                        result['nb_employees_updated'] += 1
                    else:
                        employee = self.create(data)
                        data_consultant = {
                            'company_id': company_id,
                            'lastname': line[7],
                            'firstname': line[8],
                            'simus_code': simus_code,
                            'mobile':line[19],
                            'phone':line[18],
                            'email':work_email,
                            'consultant': True,
                        }
                        if employee.job_id.name == 'Consultant':
                            consultant_id = self.env['res.partner'].create(data_consultant)
                            self.env.user.company_id.create_consultant_public_user()
                        employee_id = employee.id
                        val = '<br></br><div>' + "id: %s " % employee_id + " name: " + ustr(name) + " simus_code: %s company_id: %s" % (simus_code, company_id) + '</div>'
                        result['employees_created'] += val
                        result['nb_employees_created'] += 1
                        parent_id = self.simus_get_parent_id(data, parent_id, employee_id, result, line, company_id)
                        if parent_id:
                            employee.parent_id = parent_id
                        company['employee_simus_codes'][simus_code] = employee_id
                    contract_data = {'name': name,
                                     'wage': line[21],
                                     'employee_id': employee_id,
                                     'date_start': datetime.strptime(line[14], '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S'),
                                     'date_end': date_end,
                                     'state': 'open'}
                    contracts = employee.contract_ids.filtered(lambda contract: contract.active
                                                               ).sorted(lambda contract:
                                                                        contract.date_start, reverse=True)
                    if contracts:
                        contracts[0].write(contract_data)
                        result['nb_contracts_updated'] += 1
                    else:
                        contract = hr_contract_obj.create(contract_data)
                        val = '<br></br><div>' + "id: %s" % contract.id + " name: " + ustr(name) + " company_id: %s" % company_id + '</div>'
                        result['contracts_created'] += val
                        result['nb_contracts_created'] += 1
                else:
                    result['employees_error'] += '<br></br><div>' + "Employee error no company found: " + ustr(line) + '</div>'
            except Exception as e:
                val = '<br></br><div>' + "Employees contracts error: " + ustr(line) + "</div><br></br><div>" + "error: " + ustr(e) + "</div>"
                result['employees_error'] += val
                continue
        try:
            if lines:
                cr.commit()
        except Exception as e:
            return {'commit_error': e}
        return result