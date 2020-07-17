# -*- coding: utf-8 -*-

from odoo import fields, models


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    birthday = fields.Date(string="Birthday")
    in_position = fields.Boolean(string="In position")
    experience_level = fields.Char(string="Experience level")
    careerbuilder_code = fields.Char(string="CareerBuilder ID")
    identified_task_ids = fields.Many2many('project.task', 'applicant_task_rel', 'applicant_id',
                                           'task_id', string="Identified tasks")
    current_salary = fields.Char(string="Current salary")
    country_mobility = fields.Char(string="Country Mobility")
    region_mobility = fields.Char(string="Region Mobility")
    status = fields.Char(string="Status")
    contract_type_id = fields.Many2one('hr.contract.type', string="Contract Type")
    team_id = fields.Many2one('crm.team', string="Business Unit")