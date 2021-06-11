# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)



class ResCompany(models.Model):
    _inherit = 'res.company'

    active = fields.Boolean(string="Active", default=True)