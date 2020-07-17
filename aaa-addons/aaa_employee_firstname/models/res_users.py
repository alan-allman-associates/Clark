# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_modify_name = fields.Boolean(string="Name modified")

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super(ResUsers, self).default_get(fields_list)

        partner_model = self.env['res.partner']
        inverted = partner_model._get_inverse_name(
            partner_model._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False))

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.onchange("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for rec in self:
            rec.name = rec.partner_id._get_computed_name(
                rec.lastname, rec.firstname)

    @api.onchange("firstname", "lastname")
    def _onchange_subnames(self):
        """Avoid recursion when the user changes one of these fields.

        This forces to skip the :attr:`~.name` inversion when the user is
        setting it in a not-inverted way.
        is_modify_name is used to update name on all objects where lastname and firstname are used
        """
        # Modify self's context without creating a new Environment.
        # See https://github.com/odoo/odoo/issues/7472#issuecomment-119503916.
        self.env.context = self.with_context(skip_onchange=True).env.context
        self.is_modify_name = not self.is_modify_name

    @api.multi
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'is_modify_name' in vals:
            for user in self:
                lastname = user.lastname
                firstname = user.firstname
                employees = user.sudo().employee_ids
                employees.sudo().write({'lastname': lastname, 'firstname': firstname})
#                 employees.sudo().mapped('address_home_id').write({'lastname': lastname, 'firstname': firstname})
        return res

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if (('name' not in default) and
                ('partner_id' not in default)):
            default['name'] = _("%s (copy)") % self.name
        if 'login' not in default:
            default['login'] = _("%s (copy)") % self.login
        if (('firstname' not in default) and
                ('lastname' not in default) and
                ('name' in default)):
            default.update(self.env['res.partner']._get_inverse_name(
                default['name'], False)
            )
        return super(ResUsers, self).copy(default)
