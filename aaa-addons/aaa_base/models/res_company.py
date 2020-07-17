# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    coefficient = fields.Float(string="Average Annual Margin target")
    year_turnover_target = fields.Float(string="Annual CA target")
    year_margin_target = fields.Float(string="Annual Margin target")
    island_code = fields.Char(string="4-Island ID")
    careerbuilder_director_code = fields.Char(string="Manager CareerBuilder ID")
    careerbuilder_code = fields.Char(string="CareerBuilder ID")
    simus_code = fields.Char(string="Simus code")
    presentation = fields.Html(string="Presentation")
    site_publication = fields.Char(string="Place of publication by default")
    #TODO : change fields name in controllers
    resource = fields.Char(string="RESOURCE")
    tenant = fields.Char(string="TENANT")
    authority_host_url = fields.Char(string="AUTHORITY_HOST_URL")
    authorize_endpoint = fields.Char(string="AUTHORIZE_ENDPOINT")
    token_endpoint = fields.Char(string="TOKEN_ENDPOINT")
    client_code = fields.Char(string="CLIENT_ID")
    client_secret = fields.Char(string="CLIENT_SECRET")
    redirect_uri = fields.Char(string="REDIRECT_URI")
    api_version = fields.Char(string="API_VERSION")
    # general parameter
    coefficient_k2 = fields.Integer(string="Coefficient K2", default="2")
    billable_days = fields.Integer(string="Billable Days", default="218")
    month = fields.Integer(string="Number of Month", default="12")