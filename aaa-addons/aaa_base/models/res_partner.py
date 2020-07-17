# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartnerClone(models.Model):
    _name = "res.partner.clone"
    _rec_name = "company_name"
  
    company_name = fields.Char(string="Company")
    user_name = fields.Char(string="User")
    user = fields.Integer(string="User id")
    company = fields.Integer(string="Company id")


class ResPartner(models.Model):
    _inherit = "res.partner"

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    birthday = fields.Date(string="Date of Birth")
    linkedin_link = fields.Char(string="LinkedIn link")
    viadeo_link = fields.Char(string="Viadeo Link")
    simus_code = fields.Char(string="Simus code")
    mobility = fields.Char(string="Mobility")
    is_office = fields.Boolean(string="Is office")
    is_business_manager = fields.Boolean(string="Is business manager")
    partner_clone_ids = fields.Many2many('res.partner.clone', 'partner_clone_rel', 'partner_id', 'partner_clone_id',
                                         string="Clones", compute='_compute_partner_clone_ids', store="True",
                                         compute_sudo=True)
    is_cloned = fields.Boolean(string="Is cloned", compute='_compute_partner_clone_ids', store="True",
                               compute_sudo=True)

    @api.multi
    @api.depends('vat', 'email', 'siret', 'parent_id', 'company_id')
    def _compute_partner_clone_ids(self):
        main_company_id = self.env.ref('base.main_company').id
        partner_clone_obj = self.env['res.partner.clone']
        partner_clones = partner_clone_obj.search([])
        for part in self:
            clones = partner_clone_obj
            if not part.parent_id:
                vat = part.vat
                email = part.email
                siret = part.siret
                if vat and email and siret:
                    for partner in self.sudo().search_read([('company_id', 'not in', [part.company_id.id, main_company_id]),
                                                            ('vat', '=', vat),
                                                            ('email', '=', email),
                                                            ('siret', '=', siret),
                                                            ('is_cloned', '=', False)
                                                            ], ['company_id', 'user_id']):
                        company_id = partner['company_id'] and partner['company_id'][0]
                        user_id = partner['user_id'] and partner['user_id'][0]
                        if company_id and user_id:
                            clone = partner_clones.filtered(lambda clone: clone.company == company_id
                                                            and clone.user == user_id)
                            if not clone:
                                clone = partner_clone_obj.create({'company_name': partner['company_id'][1],
                                                                  'user_name': partner['user_id'][1],
                                                                  'company': company_id,
                                                                  'user': user_id})
                                partner_clones |= clone
                            clones |= clone
            part.update({'partner_clone_ids': [(6, 0, clones.ids)],
                         'is_cloned': bool(clones)})

    @api.model
    def recompute_partner_clone_ids(self):
        partners = self.search([])
        partners.recompute_fields(['partner_clone_ids'])
        return True
