from odoo import api, fields, models, _

class Team(models.Model):
    _inherit = 'crm.team'
    
    percent_marge_cible_team = fields.Float(string='Marge cible (%)')