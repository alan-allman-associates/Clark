# -*- coding: utf-8 -*-

from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env['res.partner']._install_partner_firstname()
        env['hr.employee']._install_employee_firstname()