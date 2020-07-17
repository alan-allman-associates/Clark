# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Speed(models.Model):
    """
    """
    _name = "speed"
    _description = "Datas speed"
    _rec_name = "user_id"

    user_id = fields.Many2one('res.users', string="User")
    partner_id = fields.Many2one('res.partner', related='user_id.partner_id', string="Partner", store=True, compute_sudo=True)
    team_id = fields.Many2one('crm.team', compute='_compute_speed_week', string="CRM Team", store=True, compute_sudo=True)
    event_ids = fields.One2many('calendar.event', 'speed_id', string="Speeds")
    year = fields.Integer(string="Year")
    month = fields.Integer(string="Month")
    week = fields.Integer(string="Week")
    speed_week = fields.Integer(compute='_compute_speed_week', string="Speed", store=True, compute_sudo=True)
    speed_week_sec = fields.Integer(compute='_compute_speed_week', string="Speed")
    prospecting = fields.Integer(compute='_compute_speed_week', string="Prospecting", store=True, compute_sudo=True)
    candidate = fields.Integer(compute='_compute_speed_week', string="Candidate", store=True, compute_sudo=True)
    qualification = fields.Integer(compute='_compute_speed_week', string="qualification", store=True, compute_sudo=True)
    commercial = fields.Integer(compute='_compute_speed_week', string="Commercial", store=True, compute_sudo=True)
    project = fields.Integer(compute='_compute_speed_week', string="Project", store=True, compute_sudo=True)

    @api.multi
    @api.depends('event_ids', 'event_ids.categ_ids', 'event_ids.user_id',
                 'event_ids.start_datetime', 'event_ids.speed_id')
    def _compute_speed_week(self):
        for speed in self:
            speed_week_sec = 0
            vals = {'project': 0,
                    'commercial': 0,
                    'qualification': 0,
                    'candidate': 0,
                    'prospecting': 0,
                    'speed_week': 0}
            for event in speed.event_ids:
                coefficient = event.coefficient or 0
                vals['speed_week'] += coefficient
                speed_week_sec += event.coefficient_sec
            vals['speed_week_sec'] = speed_week_sec
            if speed.user_id:
                crm_team = self.env['crm.team'].search([('member_ids','in',speed.user_id.ids)])
                if crm_team:
                    vals['team_id']= crm_team.id
                #speed_type = event.categ_ids.speed_type
                #if speed_type:
                    #vals[speed_type] += coefficient
            speed.update(vals)
                