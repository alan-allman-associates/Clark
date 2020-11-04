
from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


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

    def _prepare_user_datas(self, default_login):
        """ prepare user data in optic to create an user portal
        @:param default_login str
        @:return dict
        """
        user_vals = {'company_id': self.company_id.id,
                      'lastname': self.lastname,
                      'firstname': self.firstname,
                      'mobile': self.mobile,
                      'phone': self.phone,
                      'active': self.active,
                      'tz': 'Europe/Paris',
                      'login': self.email or default_login,
                      'level': 1,
                      'partner_id': self.id,
                      'notification_type': 'inbox',
                      'groups_id': [(5, 0, 0), (4, self.env.ref('base.group_public').id)],
                      'company_ids': [(6, 0, [self.company_id.id])]
                     }
        return user_vals

    def create_consultant_login(self):
        ResUsers = self.env['res.users'].with_context(no_reset_password=True)
        for consultant in self.filtered('consultant'):
            default_login = consultant.lastname + '@' + consultant.firstname + '.com'
            user = ResUsers.search([('login', 'in', [consultant.email, default_login])])
            if not user:
                vals = self._prepare_user_datas(default_login=default_login)
                user_id = ResUsers.create(vals)
                _logger.info("The user %s is successfully created", user_id.name)

    # @api.model
    # def create(self, vals):
    #     res = super(Partner, self).create(vals)
    #     if 'consultant' in vals and vals.get('consultant'):
    #         res.create_consultant_login()
    #     return res
    #
    # @api.multi
    # def write(self, vals):
    #     res = super(Partner, self).write(vals)
    #     if 'consultant' in vals and vals.get('consultant'):
    #         self.create_consultant_login()
    #     return res
