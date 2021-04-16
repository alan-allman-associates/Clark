# -*- coding: utf-8 -*-
# In post migration script:
# - we can access the registry
# - the new fields are created
# - the old fields are still readable
import logging
_logger = logging.getLogger(__name__)
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # INIT ALL
        lead_all = env['crm.lead'].search([('active', 'in', [True, False])])
        lead_all.write({'laststage_id': False})

        # INIT Gangé id = 4
        lead_all = env['crm.lead'].search([('stage_id', '=', 4)])
        _logger.info("first00 %s" % (len(lead_all.ids)))
        for lead in lead_all:
            lead.write({'laststage_id': lead.stage_id.id})
        env.cr.commit()

        # INIT perdu id [14,11]
        lead_all = env['crm.lead'].search([('type', '=', 'opportunity'), ('stage_id', 'in', [14, 11])])
        _logger.info("first0 %s" % (len(lead_all.ids)))
        for lead in lead_all:
            last_value = lead.mapped('message_ids.tracking_value_ids').filtered(
                lambda t: t.field == 'stage_id' and t.new_value_integer in [14, 11] and t.old_value_integer in [8, 5,
                                                                                                                7])
            if last_value:
                lead.write({'laststage_id': last_value.sorted(lambda x: x.id)[-1].old_value_integer})
        env.cr.commit()

        lead_all = env['crm.lead'].search(
            [('type', '=', 'opportunity'), ('probability', '=', 0), ('active', '=', False)])
        _logger.info("first1 %s" % (len(lead_all.ids)))
        for lead in lead_all:
            if lead.stage_id.id in [8, 5, 7]:
                lead.write({'laststage_id': lead.stage_id.id})
            last_value = lead.mapped('message_ids.tracking_value_ids').filtered(lambda t: t.field == 'stage_id')
            last_value = last_value and last_value.sorted(lambda x: x.id)[-1]
            if last_value.new_value_integer in [14, 11] and last_value.old_value_integer in [8, 5, 7]:
                lead.write({'laststage_id': last_value.old_value_integer})
        env.cr.commit()

        lead_all = env['crm.lead'].search(
            [('type', '=', 'opportunity'), ('lost_reason', '!=', False), ('active', '=', False)])
        _logger.info("first11 %s" % (len(lead_all.ids)))
        for lead in lead_all:
            last_value = lead.mapped('message_ids.tracking_value_ids').filtered(lambda t: t.field == 'stage_id')
            last_value = last_value and last_value.sorted(lambda x: x.id)[-1]
            if last_value.new_value_integer in [8, 5, 7]:
                lead.write({'laststage_id': last_value.new_value_integer})
        env.cr.commit()

        # INIT value of KPI

        lead_all = env['crm.lead'].search([('active', 'in', [True, False])])
        lead_all.write({'stage_25': 0, 'stage_80': 0, 'stage_50': 0, 'stage_100': 0, 'stage_all': 0})
        lead_all.write({'amount_stage_25': 0, 'amount_stage_80': 0, 'amount_stage_50': 0, 'amount_stage_100': 0})
        lead_80 = env['crm.lead'].search([('active', 'in', [True, False]), ('laststage_id', 'in', [8])])
        lead_80.write({'stage_80': 1, 'stage_all': 1})
        for lead in lead_80:
            lead.write({'amount_stage_80': lead.planned_revenue})

        lead_25 = env['crm.lead'].search([('active', 'in', [True, False]), ('laststage_id', '=', 5)])
        lead_25.write({'stage_25': 1, 'stage_all': 1})
        for lead in lead_25:
            lead.write({'amount_stage_25': lead.planned_revenue})

        lead_50 = env['crm.lead'].search([('active', 'in', [True, False]), ('laststage_id', '=', 7)])
        lead_50.write({'stage_50': 1, 'stage_all': 1})
        for lead in lead_50:
            lead.write({'amount_stage_50': lead.planned_revenue})

        lead_100 = env['crm.lead'].search([('active', 'in', [True]), ('laststage_id', '=', 4)])
        lead_100.write({'stage_100': 1, 'stage_all': 1})
        for lead in lead_100:
            lead.write({'amount_stage_100': lead.planned_revenue})
        _logger.info("FIN de traitement")
