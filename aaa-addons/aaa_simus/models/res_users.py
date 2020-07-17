# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import ustr
from datetime import datetime
import pwgen


class ResUsers(models.Model):
    _inherit = "res.users"

    simus_code = fields.Char(string="Simus code", related='partner_id.simus_code', store=True, compute_sudo=True)
    login_simus = fields.Char(string="Login simus")
    
    @api.model
    def simus_business_manager(self, cr, lines, company_simus_codes, users_login, users_simus_code, employee_obj):
        datetime_now = datetime.now()
        result = {'nb_lines': len(lines), 'nb_users_created': 0, 'nb_users_updated': 0, 'nb_employees_created': 0,
                  'nb_employees_updated': 0, 'users_error': "", 'users_created': "", 'employees_created': ""}
        for line in lines:
            
            try:
                company = company_simus_codes.get(line[1])
                if company:
                    simus_code = line[5]
                    company_id = company['id']
                    name = line[8] + " " + line[7]
                    mobile = line[19]
                    phone = line[18]
                    email = line[20].split(',')[0].strip() if '@' in line[20] else ''
                    active = True
                    if line[16] and line[16] != '0000-00-00' and datetime.strptime(line[16], '%Y-%m-%d') <= datetime_now:
                        active = False
                    user_id = users_login.get(email)
                    user_vals = {'company_id': company_id,
                                 'lastname': line[7],
                                 'firstname': line[8],
                                 'mobile': mobile,
                                 'phone': phone,
                                 'active': active,
                                 'tz': 'Europe/Paris',
#                                 'login': login,
                                 'login_simus': line[6],
                                 'level': 1,
                                 'company_ids': [(6, 0, [company_id])]}
                    vals_employee = {'company_id': company_id,
                                     'lastname': line[7],
                                     'firstname': line[8],
                                     'active': active,
                                     'work_email': email,
                                     'mobile_phone': mobile,
                                     'work_phone': phone,
                                     'user_id': user_id,
                                     'simus_code': simus_code}
                    if user_id:
                        user = self.with_context(active_test=False).browse(user_id)
                        user_vals.update({'company_ids': [(4, company_id)],
                                          'is_modify_name': not user.is_modify_name})
                        user.write(user_vals)
                        result['nb_users_updated'] += 1
                    else:
                        user_vals.update({'login': email,
                                          'password': pwgen.pwgen(12)})
                        user = self.create(user_vals)
                        user_id = user.id
                        vals_employee['user_id'] = user_id
                        val = "id: " + ustr(user_id) + " name: " + ustr(name) + " simus_code: %s company_id: %s" % (simus_code, company_id)
                        result['users_created'] += '<br></br><div>' + val + '</div>'
                        result['nb_users_created'] += 1
                    users_login[email] = user_id
                    users_simus_code[simus_code] = user_id
                    partner_vals = {'is_business_manager': True,
                                    'simus_code': simus_code}
                    user.with_context(active_test=False).partner_id.write(partner_vals)
                    employee_id = company['employee_simus_codes'].get(simus_code)
                    if employee_id:
                        employee = employee_obj.with_context(active_test=False).browse(employee_id)
                        vals_employee['is_modify_name'] = not employee.is_modify_name
                        employee.write(vals_employee)
                        result['nb_employees_updated'] += 1
                    else:
                        employee = employee_obj.create(vals_employee)
                        employee_id = employee.id
                        company['employee_simus_codes'][simus_code] = employee_id
                        val = "id: %s" % employee_id + " name: " + ustr(name) + " simus_code: %s company_id: %s" % (simus_code, company_id)
                        result['employees_created'] += '<br></br><div>' + val + '</div>'
                        result['nb_employees_created'] += 1
                else:
                    result['users_error'] += '<br></br><div>' + "User error no company found: " + ustr(line) + '</div>'
            except Exception as e:
                val = '<br></br><div>' + "Users Employees error: " + ustr(line) + "</div><br></br><div>" + "error: " + ustr(e) + '</div>'
                result['users_error'] += val
                continue
        try:
            if lines:
                cr.commit()
        except Exception as e:
            return {'commit_error': e}
        return result, users_simus_code, users_login
