
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    consultant = fields.Boolean(
        string='Consultant',
        default=False,
    )
    
    type_consultant = fields.Selection([
            ('interne', 'Interne'),
            ('pro', 'PRO'),
            ('straitant', 'Sous-traitant'),
            ('candidat', 'Candidat'),
        ],help="")
    
    
    
    consultant_skill_ids = fields.One2many(
        string='Compétences',
        comodel_name='hr.skill.partner',
        inverse_name='partner_id',
    )
    
    validate_skill_ids = fields.One2many(
        string='Compétences validées',
        comodel_name='hr.skill.partner',
        inverse_name='validate_partner_id',
    )
    
    ressources_identifiees_lead = fields.Many2many('crm.lead', 'res_partner_res_identifiees_rel', 'partner_id', 'lead_id', string='Ressources identifiées')
    ressources_envoyees_lead = fields.Many2many('crm.lead', 'res_partner_res_envoyees_rel', 'partner_id', 'lead_id', string='Ressources envoyées')
    ressources_non_retenues_lead = fields.Many2many('crm.lead', 'res_partner_res_non_retenues_rel', 'partner_id', 'lead_id', string='Ressources non retenues')
    
    ressources_identifiees_project = fields.Many2many('project.project', 'project_res_identifiees_rel', 'partner_id', 'project_id', string='Ressources identifiées')
    ressources_envoyees_project = fields.Many2many('project.project', 'project_res_envoyees_rel', 'partner_id', 'project_id', string='Ressources envoyées')
    ressources_non_retenues_project = fields.Many2many('project.project', 'project_res_non_retenues_rel', 'partner_id', 'project_id', string='Ressources non retenues')
    
    ressources_identifiees_task = fields.Many2many('project.task', 'task_res_identifiees_rel', 'partner_id', 'task_id', string='Ressources identifiées')
    ressources_envoyees_task = fields.Many2many('project.task', 'task_res_envoyees_rel', 'partner_id', 'task_id', string='Ressources envoyées')
    ressources_non_retenues_task = fields.Many2many('project.task', 'task_res_non_retenues_rel', 'partner_id', 'task_id', string='Ressources non retenues')
    
