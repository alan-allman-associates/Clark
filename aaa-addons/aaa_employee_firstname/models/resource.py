# -*- coding: utf-8 -*-

from odoo import api, fields, models
# from .. import exceptions


class ResourceResourcce(models.Model):
    _inherit = 'resource.resource'

    firstname = fields.Char(string="First name")
    lastname = fields.Char(string="Last name")
    name = fields.Char(compute="_compute_name", inverse="_inverse_name_after_cleaning_whitespace",
                       required=False, store=True, compute_sudo=True)
    is_modify_name = fields.Boolean(string="Name modified")

    @api.model
    def create(self, vals):
        """Add inverted names at creation if unavailable."""
        context = dict(self._context)
        name = vals.get("name", context.get("default_name"))
        if name:
            # Calculate the splitted fields
            inverted = self._get_inverse_name(self._get_whitespace_cleaned_name(name))
            for key, value in inverted.items():
                if not vals.get(key) or context.get("copy"):
                    vals[key] = value
            # Remove the combined fields
            if "name" in vals:
                del vals["name"]
            if "default_name" in context:
                del context["default_name"]
        return super(ResourceResourcce, self.with_context(context)).create(vals)

    @api.multi
    def write(self, vals):
        res = super(ResourceResourcce, self).write(vals)
        if 'is_modify_name' in vals:
            employee_obj = self.en['hr.employee']
            for resource in self:
                lastname = resource.lastname
                firstname = resource.firstname
                user = resource.sudo().user_id
                user.sudo().write({'lastname': lastname, 'firstname': firstname})
                employees = user.sudo().employee_ids
                employees |= employee_obj.sudo().search([('resource_id', '=', resource.id)])
                employees.sudo().write({'lastname': lastname, 'firstname': firstname})
#                 employees.sudo().mapped('address_home_id').write({'lastname': lastname, 'firstname': firstname})
        return res


    @api.multi
    def copy(self, default=None):
        """Ensure resources are copied right.
        Odoo adds ``(copy)`` to the end of :attr:`~.name`, but that would get
        ignored in :meth:`~.create` because it also copies explicitly firstname
        and lastname fields.
        """
        return super(ResourceResourcce, self.with_context(copy=True)).copy(default)

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super(ResourceResourcce, self).default_get(fields_list)
        inverted = self._get_inverse_name(self._get_whitespace_cleaned_name(result.get("name", "")))
        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)
        return result

    @api.model
    def _names_order_default(self):
        return 'first_last'

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
           You can override this method to read configuration from language,
           country, company or other"""
        return self.env['ir.config_parameter'].sudo().get_param('partner_names_order',
                                                                self._names_order_default())

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
           You can override this method to change the order of lastname and
           firstname the computed name"""
        order = self._get_names_order()
        if order == 'last_first_comma':
            return ", ".join((p for p in (lastname, firstname) if p))
        elif order == 'first_last':
            return " ".join((p for p in (firstname, lastname) if p))
        else:
            return " ".join((p for p in (lastname, firstname) if p))

    @api.multi
    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.name = record._get_computed_name(record.lastname, record.firstname)

    @api.multi
    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.
           The splitting logic is stored separately in :meth:`~._inverse_name`, so
           submodules can extend that method and get whitespace cleaning for free."""
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            # Clean name avoiding infinite recursion
            if record.name != clean:
                record.name = clean
            # Save name in the real fields
            else:
                record._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.
           Removes leading, trailing and duplicated whitespace."""
        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = ' '.join(name.decode('utf-8').split()) if name else name
        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_inverse_name(self, name):
        """Compute the inverted name.
           - Otherwise, make a guess.
            This method can be easily overriden by other submodules.
            You can also override this method to change the order of name's
            attributes    
            When this method is called, :attr:`~.name` already has unified and
            trimmed whitespace."""
        # Company name goes to the lastname
        if not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            order = self._get_names_order()
            # Remove redundant spaces
            name = self._get_whitespace_cleaned_name(
                name, comma=(order == 'last_first_comma'))
            parts = name.split("," if order == 'last_first_comma' else " ", 1)
            if len(parts) > 1:
                if order == 'first_last':
                    parts = [" ".join(parts[1:]), parts[0]]
                else:
                    parts = [parts[0], " ".join(parts[1:])]
            else:
                while len(parts) < 2:
                    parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    @api.multi
    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.name)
            record.lastname = parts['lastname']
            record.firstname = parts['firstname']

#     @api.multi
#     @api.constrains("firstname", "lastname")
#     def _check_name(self):
#         """Ensure at least one name is set."""
#         for record in self:
#             if not (record.firstname or record.lastname):
#                 raise exceptions.EmptyNamesError(record)

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


    @api.onchange("name")
    def _onchange_name(self):
        """Ensure :attr:`~.name` is inverted in the UI."""
        if self.env.context.get("skip_onchange"):
            # Do not skip next onchange
            self.env.context = (
                self.with_context(skip_onchange=False).env.context)
        else:
            self._inverse_name_after_cleaning_whitespace()
 
    # Disabling SQL constraint givint a more explicit error using a Python
    # contstraint
    _sql_constraints = [(
        'check_resource_name',
        "CHECK( 1=1 )",
        'Resource requires a name.'
    )]
