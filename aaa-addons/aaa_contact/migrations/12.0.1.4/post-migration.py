# -*- coding: utf-8 -*-
# In post migration script:
# - we can access the registry
# - the new fields are created
# - the old fields are still readable
from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def migrate(cr, version):

    _logger.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! start sript !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if not version:
        return


    with api.Environment.manage():
        accele_id = 4
        mwa_id = 19
        env = api.Environment(cr, SUPERUSER_ID, {})
        ResUsers = env['res.users']
        ResPartner = env['res.partner']
        ResCompany = env['res.company']
        CrmTeam = env['crm.team']
        CrmLead = env['crm.lead']

        accele_record = ResCompany.browse(accele_id) #res.company(4) => objet
        accele_record.write({
            'name': '[ALAN ALLMAN] F-WD'
        })

        # Res.users
        users_mwa_ids = ResUsers.search([('company_id', '=',  mwa_id)])
        users_mwa_ids.write({'company_id': accele_id, 'company_ids': [(4, accele_id)]})

        # Res.partner
        partner_mwa_ids = ResPartner.search([('company_id', '=',  mwa_id)])
        partner_mwa_ids.write({'company_id': accele_id})


        # crm.teams
        crm_team_mwa_ids = CrmTeam.search([('company_id', '=', mwa_id)])
        crm_team_mwa_ids.write({'company_id': accele_id})


        # crm.lead
        crm_lead_mwa_ids = CrmLead.search([('company_id', '=', mwa_id)])
        crm_lead_mwa_ids.write({'company_id': accele_id})

        len_partners_mwa = ResPartner.search_count([('company_id', '=', mwa_id)])
        len_users_mwa = ResUsers.search_count([('company_id', '=', mwa_id)])
        len_crm_l_mwa = CrmLead.search_count([('company_id', '=', mwa_id)])
        len_crm_t_mwa = CrmTeam.search_count([('company_id', '=', mwa_id)])
        if len_partners_mwa == len_users_mwa == len_crm_l_mwa == len_crm_t_mwa == 0:
            mwa_record = ResCompany.browse(mwa_id)
            mwa_record.active = False
            _logger.info('the company mwa is not active')

        actm_B_id = 5
        a2f_id = 2
        gb_id = 14
        actm_F_id = 6


        accele_record = ResCompany.browse(a2f_id)  # res.company(4) => objet
        accele_record.write({
            'name': '[ALAN ALLMAN] Alpha2F'
        })

        # Res.users
        users_actm_B_ids = ResUsers.search([('company_id', '=', actm_B_id)])
        users_actm_B_ids.write({'company_id': a2f_id, 'company_ids': [(4, a2f_id)]})
        users_gb_ids = ResUsers.search([('company_id', '=', gb_id)])
        users_gb_ids.write({'company_id': a2f_id, 'company_ids': [(4, a2f_id)]})
        users_actm_F_ids = ResUsers.search([('company_id', '=', actm_F_id)])
        users_actm_F_ids.write({'company_id': a2f_id, 'company_ids': [(4, a2f_id)]})

        # Res.partner
        partners_actm_B_ids = ResPartner.search([('company_id', '=', actm_B_id)])
        partners_actm_B_ids.write({'company_id': a2f_id})
        partners_gb_ids = ResPartner.search([('company_id', '=', gb_id)])
        partners_gb_ids.write({'company_id': a2f_id})
        partners_actm_F_ids = ResPartner.search([('company_id', '=', actm_F_id)])
        partners_actm_F_ids.write({'company_id': a2f_id})

        # crm.teams

        crm_team_actm_B_ids = CrmTeam.search([('company_id', '=', actm_B_id)])
        crm_team_actm_B_ids.write({'company_id': a2f_id})
        crm_team_gb_ids = CrmTeam.search([('company_id', '=', gb_id)])
        crm_team_gb_ids.write({'company_id': a2f_id})
        crm_team_actm_F_ids = CrmTeam.search([('company_id', '=', actm_F_id)])
        crm_team_actm_F_ids.write({'company_id': a2f_id})

        # crm.lead

        crm_lead_actm_B_ids = CrmLead.search([('company_id', '=', actm_B_id)])
        crm_lead_actm_B_ids.write({'company_id': a2f_id})
        crm_lead_gb_ids = CrmLead.search([('company_id', '=', gb_id)])
        crm_lead_gb_ids.write({'company_id': a2f_id})
        crm_lead_actm_F_ids = CrmLead.search([('company_id', '=', actm_F_id)])
        crm_lead_actm_F_ids.write({'company_id': a2f_id})

        # verifier
        len_partners_actm_B = ResPartner.search_count([('company_id', '=', actm_B_id)])
        len_users_actm_B = ResUsers.search_count([('company_id', '=', actm_B_id)])
        len_crm_l_actm_B = CrmLead.search_count([('company_id', '=', actm_B_id)])
        len_crm_t_actm_B = CrmTeam.search_count([('company_id', '=', actm_B_id)])
        if len_partners_actm_B == len_users_actm_B == len_crm_l_actm_B == len_crm_t_actm_B == 0:
            mwa_record = ResCompany.browse(actm_B_id)
            mwa_record.active = False
            _logger.info("the act m B company is not active")

        len_partners_gb = ResPartner.search_count([('company_id', '=', gb_id)])
        len_users_gb = ResUsers.search_count([('company_id', '=', gb_id)])
        len_crm_l_gb = CrmLead.search_count([('company_id', '=', gb_id)])
        len_crm_t_gb = CrmTeam.search_count([('company_id', '=', gb_id)])
        if len_partners_gb == len_users_gb == len_crm_l_gb == len_crm_t_gb == 0:
            mwa_record = ResCompany.browse(gb_id)
            mwa_record.active = False
            _logger.info("the gb company is not active")

        len_partners_actm_F = ResPartner.search_count([('company_id', '=', actm_F_id)])
        len_users_actm_F = ResUsers.search_count([('company_id', '=', actm_F_id)])
        len_crm_l_actm_F = CrmLead.search_count([('company_id', '=', actm_F_id)])
        len_crm_t_actm_F = CrmTeam.search_count([('company_id', '=', actm_F_id)])
        if len_partners_actm_F == len_users_actm_F == len_crm_l_actm_F == len_crm_t_actm_F == 0:
            mwa_record = ResCompany.browse(actm_F_id)
            mwa_record.active = False
            _logger.info("the act M france company is not active")

        team_accele_id = 19
        team_mwa_id = 26
        leads_mwa_ids = CrmLead.search([('team_id', 'in', [team_mwa_id])])
        if leads_mwa_ids:
            leads_mwa_ids.write({'team_id': team_accele_id})

        _logger.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! end sript !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
