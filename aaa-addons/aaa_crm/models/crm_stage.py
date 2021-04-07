# -*- coding: utf-8 -*-

from odoo import api, fields, models



class CrmStage(models.Model):
    _inherit = "crm.stage"

    is_proposal = fields.Boolean(string="Est une etape de proposition")
