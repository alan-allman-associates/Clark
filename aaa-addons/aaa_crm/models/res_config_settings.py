# Copyright 2018 Modoolar <info@modoolar.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stage_auto_id = fields.Many2one('crm.stage',
                                     config_parameter='crm.auto_stage_id')
									 

    
