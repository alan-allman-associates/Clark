from odoo import api, fields, models, _


class SearchedSkill(models.Model):
    _name = 'hr.skill.search'
    _description = 'Searched Skill'
    _rec_name = 'complete_name'

    project_id = fields.Many2one(
        string='Projet',
        comodel_name='project.project',
    )
    skill_id = fields.Many2one(
        string='Compétence',
        comodel_name='hr.skill',
    )
    
    level_required = fields.Many2one(
        string='Niveau demandé',
        comodel_name='hr.skill.level',
    )
    
    lead_id = fields.Many2one(
        string='Enjeux',
        comodel_name='crm.lead',
    )
    
    project_task_id = fields.Many2one(
        string='Mission',
        comodel_name='project.task',
    )
    
    complete_name = fields.Char(
        string='Complete Name',
        related='skill_id.complete_name',
    )
    
    description = fields.Char(
        string='Description',
        related='skill_id.description'
    )
    
    _sql_constraints = [
        (
            'project_project_skill_uniq',
            'unique(project_id, skill_id)',
            'This project already has that skill!'
        ),
        (
            'crm_lead_skill_uniq',
            'unique(lead_id, skill_id)',
            'This lead already has that skill!'
        ),
        (
            'project_task_skill_uniq',
            'unique(project_task_id, skill_id)',
            'This task already has that skill!'
        ),
    ]

    """
    @api.multi
    @api.depends('project_task_id.name','lead_id.name','project_id.name', 'skill_id.name')
    def _compute_complete_name(self):
        object_name = ''
        for consultant_skill in self:
            if consultant_skill.project_id.name :
                object_name = consultant_skill.project_id.name 
            if consultant_skill.project_task_id.name : 
                object_name = consultant_skill.project_task_id.name 
            if consultant_skill.lead_id.name : 
                object_name = consultant_skill.lead_id.name 
                
            consultant_skill.complete_name = _(
                '%(object)s, %(skill)s'
            ) % {
                'object': object_name,
                'skill': consultant_skill.skill_id.name,
            }
    """