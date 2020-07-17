# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    Part of Odoo. See LICENSE file for full copyright and licensing details.   #
#    Copyright (C) 2018 Jupical Technologies Pvt. Ltd. <http://www.jupical.com> #
#                                                                               #
#################################################################################

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    smtp_by_company = fields.Boolean(string="SMTP BY COMPANY", default=False)
    smtp_by_user = fields.Boolean(string="SMTP BY USER", default=False)

    @api.onchange('smtp_by_company')
    def onchange_smtp_config_company(self):
        if self.smtp_by_company == True:
            self.smtp_by_user = False

    @api.onchange('smtp_by_user')
    def onchange_smtp_config_user(self):
        if self.smtp_by_user == True:
            self.smtp_by_company = False

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        smtp_by_company = ICPSudo.get_param('smtp_by_user_and_company.smtp_by_company')
        smtp_by_user = ICPSudo.get_param('smtp_by_user_and_company.smtp_by_user')

        res.update(
            smtp_by_company = smtp_by_company,
            smtp_by_user = smtp_by_user
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("smtp_by_user_and_company.smtp_by_company", self.smtp_by_company)
        ICPSudo.set_param("smtp_by_user_and_company.smtp_by_user", self.smtp_by_user)
        mail_server_config = self.env['ir.mail_server'].sudo().search([])
        for mail_server in mail_server_config:
            mail_server.is_smtp_by_company =  self.smtp_by_company
            mail_server.is_smtp_by_user = self.smtp_by_user


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:ß
