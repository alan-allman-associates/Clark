# -*- coding: utf-8 -*-

from odoo import api, fields, models



class CrmLead(models.Model):
    _inherit = "crm.lead"

    is_proposal = fields.Boolean(string="Est une etape de proposition")