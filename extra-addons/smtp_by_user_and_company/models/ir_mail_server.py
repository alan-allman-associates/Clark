# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    Part of Odoo. See LICENSE file for full copyright and licensing details.   #
#    Copyright (C) 2018 Jupical Technologies Pvt. Ltd. <http://www.jupical.com> #
#                                                                               #
#################################################################################

from odoo import fields, models, api

class ir_mail_server(models.Model):

    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="User")
    company_ids = fields.Many2many('res.company','ir_mail_server_rel','mail_server_id','company_id', string="Company")
    is_smtp_by_company = fields.Boolean("Is SMTP by Company", default=False)
    is_smtp_by_user = fields.Boolean("Is SMTP by User", default=False)

    @api.model
    def default_get(self, fields):
        res = super(ir_mail_server, self).default_get(fields)
        res_config_company = self.env['res.config.settings'].search([],order='id desc', limit=1)
        if res_config_company.smtp_by_company == True:
            res.update({'is_smtp_by_company':True})
        else:
            res.update({'is_smtp_by_user':True})
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: