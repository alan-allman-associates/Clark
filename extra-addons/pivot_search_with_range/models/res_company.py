# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = "res.company"

    def search_company_read(self):
        return self.search_read([('id', 'child_of', [self.env.user.company_id.id])], ['id', 'name'])