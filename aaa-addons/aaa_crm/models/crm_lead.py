# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo import api, SUPERUSER_ID

SELECTION_AXES = [('axe1', 'Axe 1'), ('axe2', 'Axe 2'), ('axe3', 'Axe 3'), ('axe4', 'Axe 4'), ('axe5', 'Sous domaine')]

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
    axe5 = fields.Many2one('crm.axes', string="Sous domaine", domain="[('axe_type', '=', 'axe5')]")

    end_lead = fields.Datetime(string='Answer date limit')
    user_is_subdomain = fields.Boolean('IS subdomain user', compute='compute_is_subdomain')

    @api.depends('axe5')
    def compute_is_subdomain(self):
        current_user = self.env.user
        group = 'aaa_crm.axe5_sous_domain'
        for order in self:
            if current_user.id == SUPERUSER_ID:
                order.user_is_subdomain = True
            else:
                order.user_is_subdomain = current_user.has_group(group)