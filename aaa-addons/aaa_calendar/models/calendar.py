# -*- coding: utf-8 -*-

from odoo import fields, models


class CalendarEventType(models.Model):
    _inherit = "calendar.event.type"

    color = fields.Char(string="Color")


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    outlook_code = fields.Text(string="Outlook ID")
    outlook_event_code = fields.Text(string="Outlook event id")
    outlook_change_key = fields.Text(string="Outlook change key")
    outlook_url = fields.Text(string="Outlook URL")