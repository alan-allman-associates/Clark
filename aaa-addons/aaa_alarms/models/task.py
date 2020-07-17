# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_end_min = fields.Datetime(string="Date end min", compute='_compute_date_end_min', compute_sudo=True, store=True)
    is_task_max_days = fields.Datetime(string="Date end min", compute='_compute_date_end_min', compute_sudo=True, store=True)

    @api.multi
    @api.depends('date_end', 'date_start', 'date_deadline')
    def _compute_date_end_min(self):
        for task in self:
            date_end = task.date_end
            if date_end:
                task.date_end_min = date_end
            elif task.date_deadline:
                date_end_min = task.date_deadline
                task.date_end_min = str(date_end_min) + ' 23:59:59'
