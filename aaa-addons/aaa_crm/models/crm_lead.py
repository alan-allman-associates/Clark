# -*- coding: utf-8 -*-

from odoo import api, fields, models

SELECTION_AXES = [('axe1', 'Axe 1'), ('axe2', 'Axe 2'), ('axe3', 'Axe 3'), ('axe4', 'Axe 4')]

class CrmAxes(models.Model):
    _name = "crm.axes"
    _order = "axe_type, name"

    name = fields.Char(string="Value", required=True)
    axe_type = fields.Selection(SELECTION_AXES, string="Type", required=True)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    axe1 = fields.Many2one('crm.axes', string="Axe 1", domain="[('axe_type', '=', 'axe1')]")
    axe2 = fields.Many2one('crm.axes', string="Axe 2", domain="[('axe_type', '=', 'axe2')]")
    axe3 = fields.Many2one('crm.axes', string="Axe 3", domain="[('axe_type', '=', 'axe3')]")
    axe4 = fields.Many2one('crm.axes', string="Axe 4", domain="[('axe_type', '=', 'axe4')]")
    end_lead = fields.Datetime(string='Answer date limit')