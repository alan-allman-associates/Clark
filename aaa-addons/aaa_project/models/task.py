# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    simus_code = fields.Char(string="Simus Code")
    code_type = fields.Selection([('mission', 'Mission'), ('task', 'Task')], string="Type", default='mission')
