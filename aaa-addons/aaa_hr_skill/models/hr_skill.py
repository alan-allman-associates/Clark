
from odoo import api, fields, models, _


class Skill(models.Model):
    _name = 'hr.skill'
    _description = 'HR Skill'
    _parent_store = True
    _order = 'complete_name'
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Nom',
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='hr.skill',
        ondelete='cascade',
    )
    parent_path = fields.Char(
        index=True,
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
    )
    child_ids = fields.One2many(
        string='Children',
        comodel_name='hr.skill',
        inverse_name='parent_id',
    )
    employee_skill_ids = fields.One2many(
        string='Consultant(e)s',
        comodel_name='hr.skill.partner',
        inverse_name='skill_id',
    )
    description = fields.Char(
        string='Description'
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for group in self:
            if group.parent_id:
                group.complete_name = _('%(parent)s / %(own)s') % ({
                    'parent': group.parent_id.complete_name,
                    'own': group.name,
                })
            else:
                group.complete_name = group.name
                

