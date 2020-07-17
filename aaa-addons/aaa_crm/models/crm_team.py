# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    simus_code = fields.Char(string="Simus code")
