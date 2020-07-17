
from odoo import api, fields, models, _


class ConsultantSkill(models.Model):
    _name = 'hr.skill.partner'
    _description = 'Consultant Skill'
    _rec_name = 'complete_name'

    partner_id = fields.Many2one(
        string='Consultant(e)',
        comodel_name='res.partner',
    )
    skill_id = fields.Many2one(
        string='Compétence',
        comodel_name='hr.skill',
    )
    level = fields.Many2one(
        string='Niveau',
        comodel_name='hr.skill.level',
        help="Auto-évaluation"
    )
    
    level_evaluated = fields.Many2one(
        string='Niveau évalué',
        comodel_name='hr.skill.level',
        help="Évaluation expert/manager"
    )
    
    level_validate = fields.Boolean(
        string='Validée',
        default=False,
    )
    
    validate_partner_id = fields.Many2one(
        string='Compétence validée par ',
        comodel_name='res.partner',
    )
    
    complete_name = fields.Char(
        string='Nom complet',
        #compute='_compute_complete_name',
        store=True,
        related='skill_id.complete_name'
    )
    
    description = fields.Char(
        string='Description',
        related='skill_id.description'
    )

    _sql_constraints = [
        (
            'res_partner_skill_uniq',
            'unique(partner_id, skill_id)',
            'This consultant already has that skill!'
        ),
    ]

    
    
class LevelSkill(models.Model):
    _name = 'hr.skill.level'
    _description = 'HR Skill Level'
    _order = 'complete_name'
    _rec_name = 'complete_name'
    
    name = fields.Char(
        string='Nom',
        required=True,
        translate=True,
    )
    
    niveau = fields.Integer(string='Niveau', required = True)
    
    complete_name = fields.Char(
        string='Nom complet',
        compute='_compute_complete_name',
        store=True,
    )
    
    level = fields.One2many(
        string='Niveau auto-évalué',
        comodel_name='hr.skill.partner',
        inverse_name='level',
    )
    
    level_evaluated = fields.One2many(
        string='Niveau évalué',
        comodel_name='hr.skill.partner',
        inverse_name='level_evaluated',
    )
    
    level_required = fields.One2many(
        string='Niveau requis',
        comodel_name='hr.skill.search',
        inverse_name='level_required',
    )

    
    @api.depends('name', 'niveau')
    def _compute_complete_name(self):
        for group in self:
            group.complete_name = _('%(niveau)s - %(nom)s') % ({
                'niveau': group.niveau,
                'nom': group.name,
            })
            
    
