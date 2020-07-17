# -*- coding: utf-8 -*-

from odoo import _, exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=_("No name is set.")):
        self.record = record
        self._value = value
        self.name = _("Error(s) with record %s, please set a lastname or firstname.") % (self)
        self.args = (self.name, value)
