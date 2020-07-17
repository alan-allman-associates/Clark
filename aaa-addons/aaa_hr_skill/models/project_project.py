
from odoo import api, fields, models, _

class Project(models.Model):
    _inherit = 'project.project'
    
    project_skill_ids = fields.One2many(
        string='Compétences',
        comodel_name='hr.skill.search',
        inverse_name='project_id',
    )
    
    ressources_identifiees = fields.Many2many('res.partner', 'project_res_identifiees_rel', 'project_id', 'partner_id', string='Ressources identifiées')
    ressources_envoyees = fields.Many2many('res.partner', 'project_res_identifiees_rel', 'project_id', 'partner_id', string='Ressources envoyées')
    ressources_non_retenues = fields.Many2many('res.partner', 'project_res_identifiees_rel', 'project_id', 'partner_id', string='Ressources non retenues')
    
    ressources_identifiees_tes = fields.Many2many('res.partner', 'crm_lead_res_identifiees_rel_test', 'project_id', 'partner_id',related='sale_order_id.opportunity_id.ressources_identifiees', store=True)
    
    sale_order_projet = fields.One2many('sale.order', 'projet_rattache', string='Commandes liées')