# -*- coding: utf-8 -*-
from odoo import fields, models, api
import datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    speed_ids = fields.One2many('speed', 'partner_id', string="Speeds")
    speed_date = fields.Date(string="Speed date")
    is_date_current = fields.Boolean(string="Set current date")
    speed_max = fields.Integer(compute='_compute_speed_week', string="Speed maximum rate", store=True, compute_sudo=True)
    speed_week = fields.Integer(compute='_compute_speed_week', string="Speed week", store=True, compute_sudo=True)
    speed_week_sec = fields.Integer(compute='_compute_speed_week', string="Speed week sec")
    prospecting = fields.Integer(compute='_compute_speed_week', string="prospecting", store=True, compute_sudo=True)
    candidate = fields.Integer(compute='_compute_speed_week', string="", store=True, compute_sudo=True)
    qualification = fields.Integer(compute='_compute_speed_week', string="qualification", store=True, compute_sudo=True)
    commercial = fields.Integer(compute='_compute_speed_week', string="", store=True, compute_sudo=True)
    project = fields.Integer(compute='_compute_speed_week', string="", store=True, compute_sudo=True)

    @api.onchange('is_date_current')
    def onchange_is_date_current(self):
        self.update({'is_date_current': False, 'speed_date': fields.Date.today()})

    @api.multi
    @api.depends('speed_date', 'is_business_manager', 'speed_ids', 'speed_ids.event_ids',
                 'speed_ids.event_ids.categ_ids', 'speed_ids.event_ids.user_id',
                 'speed_ids.event_ids.start_datetime', 'speed_ids.event_ids.speed_id')
    def _compute_speed_week(self):
        for partner in self.filtered(lambda part: part.is_business_manager):
            speed_week_sec = 0
            date = partner.speed_date
            if date:
                year = date.year
                week = date.isocalendar()[1]
                speed_max = int(self.env.ref('aaa_speed.speed_max').sudo().value)
                vals = {'speed_week': 0,
                        'project': 0,
                        'commercial': 0,
                        'qualification': 0,
                        'candidate': 0,
                        'prospecting': 0,
                        'speed_max': speed_max}
                for speed in partner.speed_ids.filtered(lambda speed: speed.week == week and speed.year == year):
                    vals['speed_week'] +=  speed.speed_week
                    vals['project'] +=  speed.project
                    vals['commercial'] +=  speed.commercial
                    vals['qualification'] +=  speed.qualification
                    vals['candidate'] +=  speed.candidate
                    vals['prospecting'] +=  speed.prospecting
                    speed_week_sec += speed.speed_week_sec
                if not vals['speed_week']:
                    vals['speed_week'] = 1
                elif vals['speed_week'] > speed_max:
                    vals['speed_week'] = speed_max
                partner.update(vals)
                partner.speed_week_sec = speed_week_sec or 1
