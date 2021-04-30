# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import ValidationError
from email.utils import formataddr


@api.multi
def get_mail_datas(self, vals):
    uid = self._context.get('uid') or self._uid
    if uid:
        user = self.env['res.users'].sudo().browse(uid)
    else:
        user = self.env.user
    company = user.sudo().company_id
    fetchmail_server_id = vals.get('fetchmail_server_id')
    if fetchmail_server_id:
        fetchmail_server = self.env['fetchmail.server'].sudo().browse(fetchmail_server_id)
        for server in self.env['ir.mail_server'].sudo().search([('smtp_user', '=', fetchmail_server.sudo().user)], limit=1):
            message = vals.get('mail_message_id')
            if message :
                email = formataddr((company.sudo().name, server.sudo().smtp_user))
                self.env['mail.message'].sudo().browse(vals['mail_message_id']).write({'email_from': email,
                                                                                       'reply_to': email})
            return {'mail_server_id': server.id}
    mail_servers = self.env['ir.mail_server'].sudo().search([])
    for server in mail_servers.filtered(lambda server: server.sudo().is_smtp_companies):
        for server_company in server.sudo().company_ids:
            if server_company & company:
                email = formataddr((company.sudo().name, server.sudo().smtp_user))
                return {'mail_server_id': server.sudo().id,
                        'email_from': email,
                        'reply_to': email}
    for server in mail_servers.filtered(lambda server: server.sudo().is_smtp_users and server.sudo().user_id & user):
        email = formataddr((company.sudo().name, server.sudo().smtp_user))
        return {'mail_server_id': server.id,
                'email_from': email,
                'reply_to': email}
    for server in self.env['ir.mail_server'].sudo().search([('is_general', '=', True)], limit=1):
        email = formataddr((company.sudo().name, server.sudo().smtp_user))
        return {'mail_server_id': server.sudo().id,
                'email_from': email,
                'reply_to': email}
    
    return False

class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def create(self, vals):
        if not self.env.context.get('mass_mailing_server'):
            data = get_mail_datas(self, vals)
            if data:
                vals.update(data)
        return super(MailMessage, self).create(vals)

class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.model
    def create(self, vals):
        if not self.env.context.get('mass_mailing_server'):
            data = get_mail_datas(self, vals)
            if data:
                vals.update(data)
        return super(MailMail, self).create(vals)

class MassMailing(models.Model):
    """ MassMailing models a wave of emails for a mass mailign campaign.
    A mass mailing is an occurence of sending emails. """

    _inherit = 'mail.mass_mailing'

    @api.model
    def _process_mass_mailing_queue(self):
        super(MassMailing, self.with_context(mass_mailing_server=True))._process_mass_mailing_queue()


class TestMassMailing(models.TransientModel):
    _inherit = 'mail.mass_mailing.test'

    @api.multi
    def send_mail_test(self):
        return super(TestMassMailing, self.with_context(mass_mailing_server=True)).send_mail_test()
