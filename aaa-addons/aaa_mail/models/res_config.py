# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_smtp_companies = fields.Boolean(string="SMTP multi companies")
    is_smtp_users = fields.Boolean(string="SMTP multi users")

    @api.onchange('is_smtp_companies')
    def onchange_is_smtp_companies(self):
        if self.is_smtp_companies:
            self.is_smtp_users = False

    @api.onchange('is_smtp_users')
    def onchange_is_smtp_users(self):
        if self.is_smtp_users:
            self.is_smtp_companies = False

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_obj = self.env['ir.config_parameter'].sudo()
        res.update(is_smtp_companies=config_obj.get_param('aaa_mail.is_smtp_companies'),
                   is_smtp_users=config_obj.get_param('aaa_mail.is_smtp_users'))
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        is_smtp_companies = self.is_smtp_companies
        is_smtp_users = self.is_smtp_users
        config_obj = self.env['ir.config_parameter'].sudo()
        config_obj.set_param("aaa_mail.is_smtp_companies", is_smtp_companies)
        config_obj.set_param("aaa_mail.is_smtp_users", is_smtp_users)
        servers = self.env['ir.mail_server'].sudo().search([])
        servers.write({'is_smtp_companies': is_smtp_companies,
                       'is_smtp_users': is_smtp_users})
