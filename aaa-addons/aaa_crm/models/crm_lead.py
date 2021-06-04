# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError

SELECTION_AXES = [('axe1', 'Axe 1'), ('axe2', 'Axe 2'), ('axe3', 'Axe 3'), ('axe4', 'Axe 4'), ('axe5', 'Sous domaine')]

class CrmAxes(models.Model):
    _name = "crm.axes"
    _order = "axe_type, name"

    @api.model
    def _get_company(self):
        return self.env.user.company_id

    name = fields.Char(string="Value", required=True)
    axe_type = fields.Selection(SELECTION_AXES, string="Type", required=True)
    company_ids = fields.Many2many('res.company', 'res_company_axes_rel', 'axes_id', 'cid',
    string='Sociétés', default=_get_company)



class CrmLead(models.Model):
    _inherit = "crm.lead"

    axe1 = fields.Many2one('crm.axes', string="Axe 1", domain="[('axe_type', '=', 'axe1')]")
    axe2 = fields.Many2one('crm.axes', string="Axe 2", domain="[('axe_type', '=', 'axe2')]")
    axe3 = fields.Many2one('crm.axes', string="Axe 3", domain="[('axe_type', '=', 'axe3')]")
    axe4 = fields.Many2one('crm.axes', string="Axe 4", domain="[('axe_type', '=', 'axe4')]")
    axe5 = fields.Many2one('crm.axes', string="Axe 5", domain="[('axe_type', '=', 'axe5')]")
    stage_10 = fields.Integer(string="Comptage - AO")
    stage_25 = fields.Integer(string="Nb propositions émises")
    stage_50 = fields.Integer(string="Nb de qualif")
    stage_80 = fields.Integer(string="Nb de Accord verbal")
    stage_100 = fields.Integer(string="Nb de Gagné")
    stage_all = fields.Integer(string="Nbre AO total")

    amount_stage_10 = fields.Integer(string="Revenue - AO (10%)")
    amount_stage_25 = fields.Integer(string="Revenue - propositions émises (25%)")
    amount_stage_50 = fields.Integer(string="Revenue - qualif")
    amount_stage_80 = fields.Integer(string="Revenue - Accord verbal")
    amount_stage_100 = fields.Integer(string="Revenue - Gagné")
    laststage_id = fields.Many2one('crm.stage', string="Dernière étape")

    parent_id = fields.Many2one('res.partner', string="Groupe client", related="partner_id.parent_id", store=True)

    def activate_lost_leads(self):
        all_stages = self.env['crm.stage'].search([])
        lost_stage_id = self.env['crm.stage'].search([('lost_stage', '=', True)], limit=1)
        lost_leads = self.env['crm.lead'].search([('probability', '=', 0), ('active', '=', False)])
        for lead in lost_leads:
            lead.write({
                'laststage_id' : lead.stage_id.id,
                'stage_id': lost_stage_id.id,
                'active' : True,
            })
            if lead.laststage_id.id in [14, 11]:
                values = self.env['mail.message'].search([('res_id', '=', lead.id), ('author_id', '!=', 2)], order='date desc').mapped('tracking_value_ids')
                stage_value_ids = values.filtered(lambda r: r.field == 'stage_id' and r.old_value_integer not in [21, 10])
                if stage_value_ids and stage_value_ids[0].old_value_integer in all_stages.ids:
                    lead.write({'laststage_id': stage_value_ids[0].old_value_integer})
        lost_leads_sec = self.env['crm.lead'].search([('stage_id', '=', lost_stage_id.id)])
        lost_leads_sec = lost_leads_sec.filtered(lambda r: not r.laststage_id)
        for lead_sec in lost_leads_sec:
            values = self.env['mail.message'].search([('res_id', '=', lead_sec.id), ('author_id', '!=', 2)], order='date desc').mapped('tracking_value_ids')
            stage_value_ids = values.filtered(lambda r: r.field == 'stage_id' and r.old_value_integer not in [21, 10])
            if stage_value_ids and stage_value_ids[0].old_value_integer in all_stages.ids:
                    lead_sec.write({'laststage_id': stage_value_ids[0].old_value_integer})

    def update_kpi_crm_stage(self):
        for rec in self:
            vals = {'stage_25': 0, 'stage_80': 0, 'stage_50': 0, 'stage_100': 0, 'stage_all': 0,
                    'amount_stage_25': 0, 'amount_stage_80': 0, 'amount_stage_50': 0, 'amount_stage_100': 0}
            if rec.laststage_id.id == 8:
                vals.update({
                    'stage_80': 1,
                    'stage_all': 1,
                    'stage_25': 1,
                    'stage_50': 1,
                    'amount_stage_80': rec.planned_revenue,
                    'amount_stage_50': rec.planned_revenue,
                    'amount_stage_25': rec.planned_revenue
                })
            elif rec.laststage_id.id == 5:
                vals.update({
                    'stage_all': 1,
                    'stage_25': 1,
                    'amount_stage_25': rec.planned_revenue
                })
            if rec.laststage_id.id == 7:
                vals.update({
                    'stage_all': 1,
                    'stage_25': 1,
                    'stage_50': 1,
                    'amount_stage_50': rec.planned_revenue,
                    'amount_stage_25': rec.planned_revenue
                })

            elif rec.stage_id.id == 4:
                vals.update({
                    'stage_all': 1,
                    'stage_25': 1,
                    'stage_50': 1,
                    'stage_80': 1,
                    'stage_100': 1,
                    'amount_stage_80': rec.planned_revenue,
                    'amount_stage_50': rec.planned_revenue,
                    'amount_stage_25': rec.planned_revenue,
                    'amount_stage_100': rec.planned_revenue
                })
            if rec.laststage_id.id == 6:
                vals.update({
                    'stage_all': 1,
                    'stage_10': 1,
                    'amount_stage_10': rec.planned_revenue
                })
            rec.write(vals)

    def update_kpi_crm(self):
        lead_all = self.env['crm.lead'].search([])
        lead_all.write({'stage_10': 0, 'stage_25': 0, 'stage_80': 0, 'stage_50': 0, 'stage_100': 0, 'stage_all': 0})
        lead_all.write({'amount_stage_25': 0, 'amount_stage_80': 0, 'amount_stage_50': 0, 'amount_stage_100': 0})
        lead_80 = self.env['crm.lead'].search([('laststage_id', 'in', [8])])
        lead_80.write({'stage_80': 1, 'stage_all': 1, 'stage_25': 1, 'stage_50': 1})
        for lead in lead_80:
            lead.write({'amount_stage_80': lead.planned_revenue, 'amount_stage_50': lead.planned_revenue,
                        'amount_stage_25': lead.planned_revenue})
        lead_25 = self.env['crm.lead'].search([('laststage_id', '=', 5)])
        lead_25.write({'stage_25': 1, 'stage_all': 1})
        for lead in lead_25:
            lead.write({'amount_stage_25': lead.planned_revenue})

        lead_50 = self.env['crm.lead'].search([('laststage_id', '=', 7)])
        lead_50.write({'stage_50': 1, 'stage_all': 1, 'stage_25': 1})
        for lead in lead_50:
            lead.write({'amount_stage_50': lead.planned_revenue, 'amount_stage_25': lead.planned_revenue})

        lead_100 = self.env['crm.lead'].search([('stage_id', '=', 4)])
        lead_100.write({'stage_100': 1, 'stage_25': 1, 'stage_50': 1, 'stage_80': 1, 'stage_all': 1})
        for lead in lead_100:
            lead.write({'amount_stage_100': lead.planned_revenue, 'amount_stage_25': lead.planned_revenue,
                        'amount_stage_80': lead.planned_revenue,'amount_stage_50': lead.planned_revenue})

        lead_10 = self.env['crm.lead'].search([('laststage_id', '=', 6)])
        lead_10.write({'stage_10': 1, 'stage_all': 1})
        for lead in lead_10:
            lead.write({'amount_stage_10': lead.planned_revenue})

    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        lost_stage_id = self.env['crm.stage'].search([('lost_stage', '=', True)], limit=1)
        res = self.write({'active': True, 'probability': 0, 'laststage_id' : self.stage_id.id, 'stage_id': lost_stage_id.id})
        self.update_kpi_crm_stage()
        return res

    @api.multi
    def write(self, vals):
        if vals.get('stage_id'):
            stage_id = self.env['crm.stage'].browse(vals.get('stage_id'))
            if stage_id.is_proposal:
                    if not self.order_ids:
                        raise UserError(_("You can not change to this stage if you don't have an order created"))
            if stage_id.lost_stage and vals.get('probability') != 0:
                if self.probability != 0:
                    raise UserError(_("You can not change to this stage if the probability is different than 0"))
        res = super(CrmLead, self).write(vals)
        if (('laststage_id' in vals) or ('stage_id' in vals and vals.get('stage_id') and vals.get('stage_id') in [4])) and not self.env.context.get('update_axes_value'):
            self.with_context(update_axes_value=True).update_kpi_crm_stage()
        return res

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        if 'stage_id' in vals and vals.get('stage_id') and vals.get('stage_id') in [4] and not res.env.context.get('update_axes_value'):
            res.with_context(update_axes_value=True).update_kpi_crm_stage()
        return res


    end_lead = fields.Datetime(string='Answer date limit')
    user_is_subdomain = fields.Boolean('IS subdomain user', compute='compute_is_subdomain')

    @api.depends('axe5')
    def compute_is_subdomain(self):
        current_user = self.env.user
        group = 'aaa_crm.axe5_sous_domain'
        for order in self:
            if current_user.id == SUPERUSER_ID:
                order.user_is_subdomain = True
            else:
                order.user_is_subdomain = current_user.has_group(group)

#    @api.multi
#    def write(self, vals):
#        for rec in self:
#            if vals.get('stage_id'):
#                if rec.stage_id.is_proposal:
#                    if not rec.order_ids:
#                        raise UserError(_("You can not change to this stage if you don't have an order created"))


class ActivityReport(models.Model):
    """ CRM Lead Analysis """
    _inherit = "crm.activity.report"

    user_activity_id = fields.Many2one('res.users', 'Assigné à', readonly=True)

    def _select(self):
        return super(ActivityReport, self)._select() + ", m.user_activity_id"
