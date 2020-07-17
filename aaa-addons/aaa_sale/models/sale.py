# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    axe1 = fields.Many2one('crm.axes', string="Axe 1", related='opportunity_id.axe1', store=True, compute_sudo=True, readonly=True)
    axe2 = fields.Many2one('crm.axes', string="Axe 2", related='opportunity_id.axe2', store=True, compute_sudo=True, readonly=True)
    axe3 = fields.Many2one('crm.axes', string="Axe 3", related='opportunity_id.axe3', store=True, compute_sudo=True, readonly=True)
    axe4 = fields.Many2one('crm.axes', string="Axe 4", related='opportunity_id.axe4', store=True, compute_sudo=True, readonly=True)