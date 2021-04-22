# -*- coding: utf-8 -*-

from odoo import api, fields, models
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
    laststage_id = fields.Many2one('crm.stage', string="Dernière étape", store=True)

    parent_id = fields.Many2one('res.partner', string="Groupe client", related="partner_id.parent_id", store=True)

    def activate_lost_leads(self):
        lost_stage_id = self.env['crm.stage'].search([('lost_stage', '=', True)], limit=1)
        lost_leads = self.env['crm.lead'].search([('stage_id', '=', lost_stage_id.id)])
        for lead in lost_leads:
            lead.write({
                'laststage_id' : lead.stage_id.id,
                'stage_id': 14,
                'active' : True,
            })

    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        for rec in self:
            rec.update_axes_inducator()
        lost_stage_id = self.env['crm.stage'].search([('lost_stage', '=', True)], limit=1)
        return self.write({'active': True, 'probability': 0, 'laststage_id' : self.stage_id.id, 'stage_id': lost_stage_id.id})

    def fields_to_search(self):
        return [
            'stage_80',
            'stage_25',
            'stage_50',
            'stage_100',
        ]

    def update_axes_inducator(self):
        #TODO imporve this function delete id verification
        for rec in self:
            if rec.stage_id and rec.stage_id.probability and int(rec.stage_id.probability) in [25, 80, 50, 100] and rec.stage_id.id in [8 ,5, 7, 4]:
                rec.laststage_id = rec.stage_id
                for field in rec.fields_to_search():
                    rec.stage_all = 0
                    rec[field] = 0
                    rec["amount_%s" %(field)] = 0
                rec["stage_%s"%(int(rec.stage_id.probability))] = 1
                rec.stage_all = 1
                rec["amount_stage_%s" % (int(rec.stage_id.probability))] = rec.planned_revenue
            if rec.stage_id.id in [4 ,14]:
                rec.stage_10 = 1
                rec.amount_stage_10 = rec.planned_revenue
                rec.stage_all = 1


    @api.multi
    def write(self, vals):
        if 'stage_id' in vals and vals.get('stage_id') and vals.get('stage_id') in [14, 11, 4] and not self.env.context.get('update_axes_value'):
            self.with_context(update_axes_value=True).update_axes_inducator()
        if vals.get('stage_id'):
                if self.stage_id.is_proposal:
                    if not self.order_ids:
                        raise UserError(_("You can not change to this stage if you don't have an order created"))
        return super(CrmLead, self).write(vals)


    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        if 'stage_id' in vals and vals.get('stage_id') and vals.get('stage_id') in [14, 11, 4] and not res.env.context.get('update_axes_value'):
            res.with_context(update_axes_value=True).update_axes_inducator()
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
