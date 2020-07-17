from odoo import api, fields, models, _

class Task(models.Model):
    _inherit = 'project.task'
    
    project_task_skill_ids = fields.One2many(
        string='Compétences',
        comodel_name='hr.skill.search',
        inverse_name='project_task_id',
    )
    
    ressources_identifiees = fields.Many2many('res.partner', 'task_res_identifiees_rel', 'task_id', 'partner_id', string='Ressources identifiées')
    ressources_envoyees = fields.Many2many('res.partner', 'task_res_identifiees_rel', 'task_id', 'partner_id', string='Ressources envoyées')
    ressources_non_retenues = fields.Many2many('res.partner', 'task_res_identifiees_rel', 'task_id', 'partner_id', string='Ressources non retenues')