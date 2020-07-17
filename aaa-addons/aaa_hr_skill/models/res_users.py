from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    percent_marge_cible_user = fields.Float(string='Marge cible (%)')