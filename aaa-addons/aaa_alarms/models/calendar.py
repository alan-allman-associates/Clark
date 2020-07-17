# -*- coding: utf-8 -*-

from odoo import api, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    @api.model_create_multi
    def create(self, list_vals):
        return super(CalendarEvent, self).create(list_vals)
