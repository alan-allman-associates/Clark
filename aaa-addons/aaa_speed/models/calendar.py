# -*- coding: utf-8 -*-
from odoo import fields, models, api
import datetime


class CalendarEventType(models.Model):
    _inherit = "calendar.event.type"

    coefficient = fields.Integer(string="Coefficient", company_dependent=True)
    speed_type = fields.Selection([('prospecting', 'Prospecting'), ('candidate', 'Candidate'),
                                   ('qualification', 'Qualification'), ('commercial', 'Commercial'),
                                   ('project', 'Project')], string="Speed type")


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    speed_id = fields.Many2one('speed', compute='_compute_speed_id', string="Speed", store=True, compute_sudo=True)
    coefficient = fields.Integer(compute='_compute_speed_id', string="Coefficient", store=True, compute_sudo=True)
    coefficient_sec = fields.Integer(compute='_compute_speed_id', string="Coefficient sec",)

    @api.multi
    @api.depends('user_id', 'categ_ids', 'start_datetime')
    def _compute_speed_id(self):
        speed_obj = self.env['speed']
        for event in self:
            user = event.user_id
            if user.partner_id.is_business_manager:
                date = event.start_datetime
                if date:
                    user_id = user.id
                    year = date.year
                    month = date.month
                    week = date.isocalendar()[1]
                    speed = speed_obj.search([('user_id', '=', user_id), ('year', '=', year), ('week', '=', week), ], limit=1)
                    if not speed:
                        speed = speed_obj.sudo().create({'user_id': user_id,
                                                  'year': year,
                                                  'week': week,
                                                  'month': month})
                    event.update({'speed_id': speed.id, 'coefficient': sum([categ.coefficient for categ in event.categ_ids])})
                    event.coefficient_sec = sum([categ.coefficient for categ in event.categ_ids])

    @api.multi
    def unlink(self):
        for event in self:
            speed = event.speed_id
            if speed:
                speed.event_ids -= event
        return super(CalendarEvent, self).unlink()
