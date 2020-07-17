# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    simus_code = fields.Char(string="Simus Code")
    description = fields.Html(string="Description")
    income = fields.Float(string="Income")
    annual_income = fields.Float(string="Cumulates income K2")
    expenses = fields.Float(string="Cumulates charges")
    annual_expenses = fields.Float(string="Cumulates charges K2")
    result = fields.Float(string="Result")
    ca_ordered = fields.Float(string="CA Ordered")
    ca_real = fields.Float(string="CA Real")
    team_id = fields.Many2one('crm.team', string="Business Unit")
    business_manager_user_id = fields.Many2one('res.users', string="BM")