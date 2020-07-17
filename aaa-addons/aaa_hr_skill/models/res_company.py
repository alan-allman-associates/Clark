from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    percent_marge_cible_company = fields.Float(string='Marge cible (%)')