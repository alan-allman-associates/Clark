# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from datetime import datetime
import pytz


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_max_hol_id = fields.Many2one('hr.employee', string="Employee")
    employee_max_hol_ids = fields.One2many('hr.employee', 'employee_max_hol_id', string="Limit holidays")
    is_max_holidays = fields.Boolean(string="Max holidays", compute='_compute_is_max_holidays', compute_sudo=True, store=True)
    employee_max_task_id = fields.Many2one('hr.employee', string="Employee")
    employee_max_task_ids = fields.One2many('hr.employee', 'employee_max_task_id', string="Limit missions")
    employee_pro_id = fields.Many2one('hr.employee', string="Employee")
    employee_pro_ids = fields.One2many('hr.employee', 'employee_pro_id', string="Employees PRO")

    @api.multi
    @api.depends('remaining_leaves', 'company_id', 'company_id.leaves_max')
    def _compute_is_max_holidays(self):
        for employee in self:
            if employee.remaining_leaves > 0:
                leaves_max = employee.company_id.leaves_max
                if leaves_max and leaves_max <= employee.remaining_leaves:
                    employee.is_max_holidays = True

    @api.model
    def _get_datetime_utc(self, date_timezone, timezone):
        local = pytz.timezone(timezone)
        date = datetime.strptime(date_timezone, DTF)
        local_dt = local.localize(date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        return datetime.strftime(utc_dt, DTF)

    @api.model
    def get_aaa_alarms(self):
        company_obj = self.env['res.company']
        employee_obj = self.browse()
        task_company_ids = holi_company_ids = []
        company_task_day_max = {}
        for company in company_obj.search_read([('parent_id', '!=', False), '|',
                                                ('leaves_max', '>', 0), ('task_day_max', '>', 0)],
                                               ['leaves_max', 'task_day_max']):
            company_id = company['id']
            if company['leaves_max']:
                holi_company_ids += [company_id]
            if company['task_day_max']:
                task_company_ids += [company_id]
                company_task_day_max[company_id] = company['task_day_max']
        holi_companies = company_obj.browse(list(set(holi_company_ids)))
        task_companies = company_obj.browse(list(set(task_company_ids)))

        employees = self.search([('employee_max_hol_id', '!=', False), ('employee_max_task_id', '!=', False),
                                 ('employee_pro_id', '!=', False)])
        employees.write({'employee_max_hol_id': False, 'employee_max_task_id': False,
                         'employee_pro_id': False})
        values = []
        event_values = {'privacy': 'confidential',
                        'show_as': 'free',
                        'alarm_ids': [(6, 0, [self.env.ref('aaa_alarms.alarm_notif_aaa').id])]
                        }
        today = fields.Date.today()
        today_string = today.strftime(DF)
        datetime_alarm_start = today_string + ' ' + self.env.ref('aaa_alarms.aaa_alarm_start').sudo().value
        datetime_alarm_stop = today_string + ' ' + self.env.ref('aaa_alarms.aaa_alarm_end').sudo().value
        employee_obj = self.env['hr.employee']
        for user in self.env['res.users'].search([('is_business_manager', '=', True), ('email', '!=', '')]):
            holi_user_companies = user.company_ids & holi_companies
            task_user_companies = user.company_ids & task_companies
            user_id = user.id
            child_temp_employees = employee_obj
#             bm_employees = user.employee_ids.mapped('child_filter_ids')
            bm_employee_ids = user.employee_ids._search([])
            if bm_employee_ids:
                bm_employees = employee_obj.browse(bm_employee_ids)
                parent_holi_by_company = {}
                for company in holi_user_companies:
                    for employee in bm_employees.filtered(lambda emp: emp.parent_id.is_business_manager and emp.company_id & company ):
                        parent_holi_by_company[company.id] = employee.parent_id.id
                        break
                parent_task_by_company = {}
                for company in task_user_companies:
                    for employee in bm_employees.filtered(lambda emp: emp.parent_id.is_business_manager and emp.company_id & company):
                        parent_task_by_company[company.id] = employee.parent_id.id
                        break
#                 test = True
#                 child_temp_employees = bm_employees
#                 while test:
#                     childs_of_childs = child_temp_employees.mapped('child_ids')
#                     if childs_of_childs:
#                         bm_employees |= childs_of_childs
#                         child_temp_employees = childs_of_childs
#                     else:
#                         test = False
                tasks_employees = pro_employees = employee_obj
                for employee in bm_employees.filtered(lambda emp: emp.company_id & task_user_companies):
                    task_ids = employee.user_id.task_ids
                    tasks = task_ids.filtered(lambda task: task.code_type == 'misssion'
                                              and task.date_start.date() <= today
                                              and task.date_end_min.date() >= today
                                              ).sorted(key=lambda task: task.date_end_min)
                    if tasks:
                        company_id = employee.company_id.id
                        delta = tasks[0].date_end_min.date() - today
                        if company_id in company_task_day_max and company_task_day_max[company_id] >= delta.days:
                            tasks_employees |= employee
                    else:
                        pro_employees |= employee
                has_tasks = has_pros = False
                for company in task_user_companies:
                    company_id = company.id
                    parent_id = company_id in parent_task_by_company and parent_task_by_company[company_id]
                    if parent_id:
                        company_employees = tasks_employees.filtered(lambda emp: emp.company_id & company)
                        if company_employees:
                            company_employees.write({'employee_max_task_id': parent_id})
                            has_tasks = True
                        company_employees = pro_employees.filtered(lambda emp: emp.company_id & company)
                        if company_employees:
                            company_employees.write({'employee_pro_id': parent_id})
                            has_pros = True
                self = self.with_context(lang=user.lang, tz=user.tz)
                description = ""
                if has_tasks:
                    description += _("you have employee(s) near limit date end mission") + "\n"
                if has_pros:
                    description += _("you have employee(s) who are PRO") + "\n"
                holidays_employees = bm_employees.filtered(lambda emp: emp.is_max_holidays)
                for company in holi_user_companies:
                    company_employees = holidays_employees.filtered(lambda emp: emp.company_id & company)
                    company_id = company.id
                    if company_employees and company_id in parent_holi_by_company:
                        company_employees.write({'employee_max_hol_id': parent_holi_by_company[company_id]})
                if holidays_employees:
                    description += _("you have employee(s) who reached days max limit holidays") + "\n"
                all_employees = holidays_employees | tasks_employees | pro_employees
                if all_employees:
                    description_company = _("for company(ies)")
                    for employee in all_employees:
                        company_name = employee.company_id.name
                        if company_name not in description_company:
                            description_company += " %s," % company_name
                    description_company = description_company[:-1]
                    description += description_company
                    timezone = user.tz
                    vals = event_values.copy()
                    vals.update({'name': _("Employees Alarm"),
                                 'user_id': user_id,
                                 'description': description,
                                 'start': self._get_datetime_utc(datetime_alarm_start, timezone),
                                 'stop': self._get_datetime_utc(datetime_alarm_stop, timezone),
                                 'partner_ids': [(6, 0, [user.partner_id.id])]})
                    values += [vals]
        if values:
            self.env['calendar.event'].create(values)
