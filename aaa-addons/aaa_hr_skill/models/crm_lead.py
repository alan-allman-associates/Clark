from odoo import api, fields, models, _

class Lead(models.Model):
    _inherit = 'crm.lead'
    
    idees_folles = fields.Html('Idées folles')
    lead_skill_ids = fields.One2many(
        string='Compétences',
        comodel_name='hr.skill.search',
        inverse_name='lead_id',
    )
    
    ressources_identifiees = fields.Many2many('res.partner', 'res_partner_res_identifiees_rel', 'lead_id', 'partner_id', string='Ressources identifiées')
    ressources_envoyees = fields.Many2many('res.partner', 'res_partner_res_envoyees_rel', 'lead_id', 'partner_id', string='Ressources envoyées')
    ressources_non_retenues = fields.Many2many('res.partner', 'res_partner_res_non_retenues_rel', 'lead_id', 'partner_id', string='Ressources non retenues')
    
    
    order_line_ids = fields.One2many('sale.order.line','opportunity_id',string="Propositions")
    number_of_days = fields.Float(string="Nombre de jour", compute="_compute_number_of_days", store=True)

    @api.depends('order_line_ids.product_uom_qty')
    def _compute_number_of_days(self):
        for rec in self:
            nb_days = sum([ line.product_uom_qty for line in rec.order_line_ids])
            rec.number_of_days = nb_days