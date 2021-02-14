# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MailMessage(models.Model):
    _inherit = 'mail.message'

    user_activity_id = fields.Many2one('res.users', 'Assigné à')

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def action_feedback(self, feedback=False):
        user_activity_id = self.sudo().user_id
        message = self.env['mail.message']
        message_id = super(MailActivity, self).action_feedback(feedback=feedback)
        if message_id:
            mail_message_id = message.browse(message_id)
            mail_message_id.sudo().user_activity_id = user_activity_id
        return message_id