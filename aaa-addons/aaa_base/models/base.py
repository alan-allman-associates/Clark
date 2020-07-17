# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import UserError


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.multi
    def recompute_fields(self, fnames):
        for fname in fnames:
            field = self._fields[fname]
            if getattr(field, 'store') and getattr(field, 'compute'):
                self._recompute_todo(field)
            else:
                raise UserError(_('%s is not a stored compute/function field')
                                % fname)
        self.recompute()
        return True