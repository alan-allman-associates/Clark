# -*- coding: utf-8 -*-
# Copyright (C) 2021 - Auguria (<https://www.auguria.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import itertools
from io import StringIO, BytesIO
import base64
import csv
import codecs
from odoo import api, fields, models, _
DATE_FORMAT = '%d/%m/%Y'

class HrWriter(object):

    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
date_range_selection = [
    ('today', _('Today')),
    ('this_week',_('This Week')),
    ('this_month', _('This Month')),
    ('this_quarter', _('This Quarter')),
    ('this_year', _('This Year')),
    ('yesterday', _('Yesterday')),
    ('last_week', _('Last Week')),
    ('last_month', _('Last Month')),
    ('last_quarter', _('Last Quarter')),
    ('last_year', _('Last Year')),
    ('last_7_days',_('Last 7 Days')),
    ('last_30_days', _('Last 30 Days')),
    ('last_365_days',_('Last 365 Days'))
]

class CrmKpi(models.TransientModel):
    _name = 'crm.kpi'
    _description = 'CRM KPI'

    axe1 = fields.Many2one('crm.axes', string="Domaine", domain="[('axe_type', '=', 'axe1')]")
    axe2 = fields.Many2one('crm.axes', string="Type", domain="[('axe_type', '=', 'axe2')]")
    axe3 = fields.Many2one('crm.axes', string="Périmètre", domain="[('axe_type', '=', 'axe3')]")
    axe4 = fields.Many2one('crm.axes', string="Engagement", domain="[('axe_type', '=', 'axe4')]")
    axe5 = fields.Many2one('crm.axes', string="Sous domaine", domain="[('axe_type', '=', 'axe5')]")
    company_id = fields.Many2one('res.company', 'Cabinet')
    date_range = fields.Selection(string="Date clôture", selection=date_range_selection)

    def fields_to_search(self):
        return [
            'axe1',
            'axe2',
            'axe3',
            'axe4',
            'axe5',
            'company_id',
        ]

    def action_crm_kpi(self):
        action = self.env.ref('aaa_crm.crm_opportunity_action_crm_kpi').read()[0]
        ctx = {'active_test': True, 'active_id': False, 'active_ids': False, 'search_disable_custom_filters': False}
        for field in self.fields_to_search():
            if self[field]:
                ctx['search_default_%s' %(field)] = self[field].id
        if self.date_range:
            ctx['time_ranges'] = {'field': 'date_closed', 'range': self.date_range}
        if ctx:
            action['context'] = ctx
        return action
