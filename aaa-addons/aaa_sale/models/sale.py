# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    axe1 = fields.Many2one('crm.axes', string="Axe 1", related='opportunity_id.axe1', store=True, compute_sudo=True, readonly=True)
    axe2 = fields.Many2one('crm.axes', string="Axe 2", related='opportunity_id.axe2', store=True, compute_sudo=True, readonly=True)
    axe3 = fields.Many2one('crm.axes', string="Axe 3", related='opportunity_id.axe3', store=True, compute_sudo=True, readonly=True)
    axe4 = fields.Many2one('crm.axes', string="Axe 4", related='opportunity_id.axe4', store=True, compute_sudo=True, readonly=True)
    
    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        enjeu_id = values.get('opportunity_id')
        config = self.env['ir.config_parameter']
        stage_id =  int(config.get_param('crm.auto_stage_id'))
        if stage_id and enjeu_id:
            query = """
                        UPDATE crm_lead
                        SET    stage_id = %(stage_id)s 
                        WHERE  id = %(enjeu_id)s
                    """
            self._cr.execute(query, {'stage_id' : stage_id, 'enjeu_id' : enjeu_id})
        return res
