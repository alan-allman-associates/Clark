# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    Part of Odoo. See LICENSE file for full copyright and licensing details.   #
#    Copyright (C) 2018 Jupical Technologies Pvt. Ltd. <http://www.jupical.com> #
#                                                                               #
#################################################################################

from odoo import fields, models, api


class Mail(models.Model):

    _inherit = "mail.mail"

    @api.model
    def create(self, vals):

        user = False

        if 'uid' in self._context:
            user = self.env['res.users'].browse(
                self._context.get('uid'))
        elif self.env.user:
            user = self.env.user
        elif self._uid:
            user = self.env['res.users'].browse(self._uid)

        ICPSudo = self.env['ir.config_parameter'].sudo()

        smtp_by_company = bool(ICPSudo.get_param(
            'smtp_by_user_and_company.smtp_by_company'))
        smtp_by_user = bool(ICPSudo.get_param(
            'smtp_by_user_and_company.smtp_by_user'))

        if smtp_by_company:
            out_mail_sever = self.env['ir.mail_server'].search(
                [('company_ids', '=', user.company_id.id)], limit=1)
        elif smtp_by_user:
            out_mail_sever = self.env['ir.mail_server'].search(
                [('user_id', '=', user.id)], limit=1)
        else:
            return super(Mail, self).create(vals)

        if out_mail_sever:
            email_from = user.partner_id.name + " " + "<" + out_mail_sever.smtp_user + ">"
            reply_to = user.partner_id.name + " " + "<" + \
                user.partner_id.email or out_mail_sever.smtp_user
            vals.update({'mail_server_id': out_mail_sever.id,
                         'email_from': email_from, 'reply_to': reply_to})

        result = super(Mail, self).create(vals)
        return result


class MailMessage(models.Model):

    _inherit = "mail.message"

    @api.model
    def create(self, vals):
        user = False
 
        if 'uid' in self._context:
            user = self.env['res.users'].browse(
                self._context.get('uid'))
        elif self.env.user:
            user = self.env.user
        elif self._uid:
            user = self.env['res.users'].browse(self._uid)
 
        active_company_id = self.env.user.company_id and self.env.user.company_id.id
        mail_server = self.env['ir.mail_server'].sudo().search(
            [('is_smtp_by_company', '=', True)])
        if mail_server:
            out_mail_sever = self.env['ir.mail_server'].sudo().search([])
            for mail_server in out_mail_sever:
                for company in mail_server.company_ids:
                    if active_company_id == company.id:
                        vals.update({'mail_server_id': mail_server.id})
        else:
            out_mail_sever = self.env['ir.mail_server'].sudo().search(
                [('user_id', '=', user.id)])
            if out_mail_sever:
                vals.update({'mail_server_id': out_mail_sever.id})
 
        result = super(MailMessage, self).create(vals)
        return result
