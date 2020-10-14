# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    manage_speed = fields.Boolean(string="Manage Speed", default=True, store=True)
 
