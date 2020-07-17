# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    time_job = fields.Selection([('full', 'Full time'), ('part', 'Part time')], string="Time job")
    last_interview = fields.Date(string="Last interview")
    cost_k2 = fields.Float(string="K2 cost", compute='_cost_k2', store=True, compute_sudo=True)
    daily_fee = fields.Float(string="Average daily fee")
    annual_target_k2 = fields.Float(string="Annual target K2")
    careerbuilder_code = fields.Char(string="Careerbuilder Id")
    careerbuilder_user_code = fields.Char(string="Careerbuilder user id")
    simus_manager_code = fields.Char(string="Simus Manager ID")
    simus_code = fields.Char(string="Simus code")
    is_departure_probability = fields.Boolean(string="Departure probability")
    is_business_manager = fields.Boolean(string="Is business manager", related='user_id.partner_id.is_business_manager',
                                         store=True, compute_sudo=True)
    leaves_previous_year = fields.Float(string="Vacation previous year")
    leaves_current_year = fields.Float(string="Vacation current year")
    leaves_employer = fields.Float(string="Other Vacation employer")
    leaves_employee = fields.Float(string="Other Vacation employee")
    remaining_leaves = fields.Float(compute='_compute_remaining_leaves', string='Remaining Legal Leaves',
                                    compute_sudo=True, store=True,
                                    help='Total number of legal leaves allocated to this employee, change this value to create'
                                         ' allocation/leave request. Total based on all the leave types without overriding limit.')
#     child_filter_ids = fields.Many2many('hr.employee', 'employee_childs_rel', 'employee_id', 'child_id', string="Subordinates",
#                                         compute='_compute_child_filter_ids', store=True, compute_sudo=True)

#     @api.model
#     def recompute_employee_ids(self):
#         cr =self._cr
#         cr.execute("""SELECT id from hr_employee""")
#         employees = self.sudo().with_context(active_test=False).browse([res[0] for res in cr.fetchall()])
#         for employee in employees:
#             employee.recompute_fields(['child_filter_ids'])
#         return True
#  
#     @api.multi
#     def write(self, vals):
#         res = super(HrEmployee, self).write(vals)
#         self.recompute_employee_ids()
#         return res

#     @api.multi
#     @api.depends('parent_id', 'company_id')
#     def _compute_child_filter_ids(self):
#         for emp in self:
#             employee_id = emp.id
#             cr = self._cr
#             cr.execute("""SELECT employee_id FROM employee_childs_rel WHERE child_id = %s""", (employee_id, ))
#             parent_ids = [val[0] for val in cr.fetchall()]
#             for parent_id in parent_ids:
#                 self.browse(parent_id)._write({'child_filter_ids': [(3, employee_id)]})
#             parent = emp.parent_id
#             while parent:
#                 if emp.company_id & parent.company_id:
#                     parent._write({'child_filter_ids': [(4, employee_id)]})
#                 parent = parent.parent_id

    # override native method in module hr_holidays
    @api.multi
    @api.depends('leaves_previous_year', 'leaves_current_year', 'leaves_employer', 'leaves_employee')
    def _compute_remaining_leaves(self):
        for employee in self:
            remaining_leaves = employee.leaves_previous_year or 0 + employee.leaves_current_year or 0 + \
                               employee.leaves_employer or 0 + employee.leaves_employee or 0
            employee.remaining_leaves = float_round(remaining_leaves, precision_digits=2)

    @api.onchange('company_id')
    def _onchange_company(self):
        user = self.env.user
        if self.company_id and not self.company_id & user.company_id and not user & self.env.ref('base.user_root'):
            raise UserError(_('You can not change value of the company'))
        return super(HrEmployee, self)._onchange_company()

    @api.multi
    @api.depends('contract_ids', 'contract_ids.date_start',
                 'contract_ids.active', 'contract_ids.wage',
                 'contract_ids.employee_id')
    def _cost_k2(self):
        for employee in self:
            cost = 0
            for contract in self.env['hr.contract'].search([('employee_id', '=', employee.id)],
                                                           order='date_start desc', limit=1):
                cost = (contract.wage * 12 * 2) / 218
            employee.cost_k2 = cost

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user
        if self.env.ref('base.user_root') + self.env.ref('base.user_admin') & user:
            return super(HrEmployee, self).search(args, offset=offset, limit=limit, order=order, count=count)
        res = super(HrEmployee, self).search(args, offset=offset, limit=0, order=order, count=count)
        if not count and res:
            if not (self.env.ref('aaa_security.aaa_general_direction').mapped('users') & user):
                groups = self.env.ref('aaa_security.aaa_office_director') + self.env.ref('aaa_security.aaa_bu_director') + \
                         self.env.ref('aaa_security.aaa_bm')
                if groups.mapped('users') & user:
                    employees = user.employee_ids
                    childs = employees.child_ids
                    while childs:
                        employees += childs
                        childs = childs.mapped('child_ids')
                    employees |= res.filtered(lambda emp: not emp.parent_id and not emp.child_ids)
                    employees = res & employees
                    res = employees
                else:
                    res = res & user.employee_ids
        if not count and res:
            res = res.filtered(lambda emp: emp.company_id & user.company_id)
            if not order:
                res = res.sorted(key=lambda emp: emp.name)
            super(HrEmployee, self).search(args, offset=offset, limit=limit, order=order, count=count)
        return res
