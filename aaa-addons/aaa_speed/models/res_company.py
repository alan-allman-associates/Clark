# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    manage_speed = fields.Boolean(string="Manage Speed", default=True, store=True)
 
    @api.onchange('manage_speed')
    def _onchange_manage_speed(self):
		group = self.env.ref('aaa_speed.group_manage_speed')
        users = self.env['res.users'].search([('company_id', '=', self.id)])
		if manage_speed:
		   for user in users:
		       group.write({
			   [(4, user.id)]
			   })
		else:
		   for user in users:
		       group.write({
			   [(3, user.id)]
			   })
