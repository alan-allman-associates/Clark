# -*- coding: utf-8 -*-

from odoo import fields, models, api

class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="User")
    company_ids = fields.Many2many('res.company', 'ir_mail_server_company_rel', 'mail_server_id','company_id',
                                   string="Companies")
    is_smtp_companies = fields.Boolean(string="Is SMTP companies")
    is_smtp_users = fields.Boolean(string="Is SMTP users")
    is_general = fields.Boolean(string="Is general")

    @api.model
    def default_get(self, default_fields):
        res = super(IrMailServer, self).default_get(default_fields)
        res_config = self.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if res_config.is_smtp_companies:
            res['is_smtp_companies'] = True
        else:
            res['is_smtp_users'] = True
        return res

    @api.one
    def _update_is_general(self, vals):
        self.ensure_one()
        if vals.get('is_general'):
            for server in self.search([('id', '!=', self.id), ('is_general', '=', True)]):
                server.is_general = False

    @api.multi
    def write(self, vals):
        res = super(IrMailServer, self).write(vals)
        for record in self:
            record._update_is_general(vals)
        return res

    @api.model
    def create(self, vals):
        res = super(IrMailServer, self).create(vals)
        if vals.get('is_general'):
            res._update_is_general(vals)
        return res
