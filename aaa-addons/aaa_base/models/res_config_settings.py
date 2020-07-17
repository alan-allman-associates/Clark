# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

#     careerbuilder_site_url = fields.Char(string="Url Site Careerbuilder", config_parameter='aaa_base.careerbuilder_site_url')
#     careerbuilder_api_url = fields.Char(string="Url Api Careerbuilder", config_parameter='aaa_base.careerbuilder_api_url')
#     careerbuilder_api_user = fields.Char(string="Api Careerbuilder User", config_parameter='aaa_base.careerbuilder_api_user')
#     careerbuilder_api_password = fields.Char(string="Api Careerbuilder Password", config_parameter='aaa_base.careerbuilder_api_password')
#     simus_url_api = fields.Char(string="Url Api Simus", config_parameter='aaa_base.simus_url_api')
#     simus_url_apikey = fields.Char(string="Url Api Simus Key", config_parameter='aaa_base.simus_url_apikey')
#     mantis_user = fields.Char(string="Mantis User", config_parameter='aaa_base.mantis_user')
#     mantis_password = fields.Char(string="Mantis Password", config_parameter='aaa_base.mantis_password')
#     mantis_url = fields.Char(string="Mantis Url", config_parameter='aaa_base.mantis_url')
#     mantis_project_code = fields.Char(string="Mantis Project ID", config_parameter='aaa_base.mantis_project_code')
    billable_days = fields.Integer(string="Billable Days", related='company_id.billable_days', readonly=False, store=True, compute_sudo=True)
    coefficient_k2 = fields.Integer(string="Coefficient K2", related='company_id.coefficient_k2', readonly=False, store=True, compute_sudo=True)
    month = fields.Integer(string="Number of Month", related='company_id.month', readonly=False, store=True, compute_sudo=True)
