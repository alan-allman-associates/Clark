# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    outlook_ident = fields.Char(string="Outlook identify")
    outlook_password= fields.Char(string="Outlook password")
    outlook_token = fields.Char(string="Outlook token")
    outlook_server = fields.Char(string="Outlook server")
    career_builder_trigram = fields.Char(string="Career builder trigam")
    is_buddy = fields.Boolean(string="Buddy")
    concerning = fields.Html(string="About")
    rank = fields.Integer(string="Rank")
    annual_target_k2 = fields.Float(string="Annual target k2")
    #TODO verify attribute selection
    level = fields.Selection([(1, 'Beginner'), (2, 'intermediate'),
                              (3, 'Advanced'), (4, 'Expert'), (5, 'Superman')], string="Level")
    synchronization_outlook_mail = fields.Selection([('manual','Manual'), ('auto','Automatic')],
                                                    string="Synchronization mail outlook", default='manual')
    synchronization_outlook_calendar = fields.Selection([('manual','Manual'), ('all','All '), ('tagged','Tagged only ')],
                                                        string="Synchronization calendar outlook", default='manual')
    is_refresh_token = fields.Boolean(string="Refresh Token", size="512")
    is_business_manager = fields.Boolean(string="Is business manager", related='partner_id.is_business_manager',
                                         store=True, compute_sudo=True)