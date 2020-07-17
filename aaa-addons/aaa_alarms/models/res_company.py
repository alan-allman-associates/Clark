# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    leaves_max = fields.Float(string="Maximum leaves")
    task_day_max = fields.Float(string="End mission max days")
