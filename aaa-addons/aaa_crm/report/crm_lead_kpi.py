# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api

from odoo.addons.crm.models import crm_stage

class CrmLeadKpiCompany(models.Model):
    """ Crm Lead Kpi Company """

    _name = "crm.lead.kpi.company"
    _auto = False
    _description = "Crm Lead Kpi Company"

    date_closed = fields.Datetime('Date du clôture', readonly=True)
    axe1 = fields.Many2one('crm.axes', string="Domaine", domain="[('axe_type', '=', 'axe1')]")
    axe2 = fields.Many2one('crm.axes', string="Type", domain="[('axe_type', '=', 'axe2')]")
    axe3 = fields.Many2one('crm.axes', string="Périmètre", domain="[('axe_type', '=', 'axe3')]")
    axe4 = fields.Many2one('crm.axes', string="Engagement", domain="[('axe_type', '=', 'axe4')]")
    axe5 = fields.Many2one('crm.axes', string="Sous domaine", domain="[('axe_type', '=', 'axe5')]")
    stage_10 = fields.Integer(string="Comptage - A1O")
    stage_25 = fields.Integer(string="Nb propositions émises")
    stage_50 = fields.Integer(string="Nb de qualif")
    stage_80 = fields.Integer(string="Nb de Accord verbal")
    stage_100 = fields.Integer(string="Nb de Gagné")
    stage_all = fields.Integer(string="Nbre AO total")
    company_id = fields.Many2one('res.company', string="Cabinet")
    amount_stage_10 = fields.Integer(string="Revenue - AO (10%)")
    amount_stage_25 = fields.Integer(string="Revenue - propositions émises (25%)")
    amount_stage_50 = fields.Integer(string="Revenue - qualif")
    amount_stage_80 = fields.Integer(string="Revenue - Accord verbal")
    amount_stage_100 = fields.Integer(string="Revenue - Gagné")
    laststage_id = fields.Many2one('crm.stage', string="Dernière étape", store=True)
    stage_id = fields.Many2one('crm.stage', string="Etape")
    parent_id = fields.Many2one('res.partner', string="Groupe client")
    partner_id = fields.Many2one('res.partner', string="Client")
    team_id = fields.Many2one('crm.team', string='Equipe commerciale')
    user_id = fields.Many2one('res.users', string="Vendeur")



    def _select(self):
        select_str = """
        SELECT
            c.id,
            c.date_closed AS date_closed,
            c.axe1 AS axe1,
            c.axe2 AS axe2,
            c.axe3 AS axe3,
            c.axe4 AS axe4,
            c.axe5 AS axe5,
            c.stage_10 AS stage_10,
            c.stage_25 AS stage_25,
            c.stage_50 AS stage_50,
            c.stage_80 AS stage_80,
            c.stage_100 AS stage_100,
            c.stage_all AS stage_all,
            c.company_id AS company_id,
            c.amount_stage_10 AS amount_stage_10,
            c.amount_stage_25 AS amount_stage_25,
            c.amount_stage_50 AS amount_stage_50,
            c.amount_stage_80 AS amount_stage_80,
            c.amount_stage_100 AS amount_stage_100,
            c.laststage_id AS laststage_id,
            c.stage_id AS stage_id,
            c.parent_id AS parent_id,
            c.team_id AS team_id,
            c.user_id AS user_id,
            c.partner_id AS partner_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM crm_lead AS c
        """
        return from_str

    def _join(self):
        join_str = """
            LEFT JOIN "crm_stage" stage ON stage.id = c.stage_id
        """
        return join_str

    def _where(self):
        where_str = """
         WHERE
                c.type = 'opportunity' AND c.active = True
           
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY c.id,
            date_closed,
            axe1,
            axe2,
            axe3,
            axe4,
            axe5,
            stage_10,
            stage_25,
            stage_50,
            stage_80,
            stage_100,
            stage_all,
            company_id,
            amount_stage_10,
            amount_stage_25,
            amount_stage_80,
            amount_stage_50,
            amount_stage_100,
            laststage_id,
            stage_id,
            parent_id,
            team_id,
            user_id,
            partner_id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE VIEW %s AS (
            %s
            %s
            %s
            %s
        )""" % (self._table, self._select(), self._from(), self._where(), self._group_by()))


class CrmLeadKpiCustomer(models.Model):
    """ Crm Lead Kpi Company """

    _name = "crm.lead.kpi.customer"
    _auto = False
    _description = "Crm Lead Kpi Customer"

    date_closed = fields.Datetime('Date du clôture', readonly=True)
    axe1 = fields.Many2one('crm.axes', string="Domaine", domain="[('axe_type', '=', 'axe1')]")
    axe2 = fields.Many2one('crm.axes', string="Type", domain="[('axe_type', '=', 'axe2')]")
    axe3 = fields.Many2one('crm.axes', string="Périmètre", domain="[('axe_type', '=', 'axe3')]")
    axe4 = fields.Many2one('crm.axes', string="Engagement", domain="[('axe_type', '=', 'axe4')]")
    axe5 = fields.Many2one('crm.axes', string="Sous domaine", domain="[('axe_type', '=', 'axe5')]")
    stage_10 = fields.Integer(string="Comptage - A1O")
    stage_25 = fields.Integer(string="Nb propositions émises")
    stage_50 = fields.Integer(string="Nb de qualif")
    stage_80 = fields.Integer(string="Nb de Accord verbal")
    stage_100 = fields.Integer(string="Nb de Gagné")
    stage_all = fields.Integer(string="Nbre AO total")
    company_id = fields.Many2one('res.company', string="Cabinet")
    amount_stage_10 = fields.Integer(string="Revenue - AO (10%)")
    amount_stage_25 = fields.Integer(string="Revenue - propositions émises (25%)")
    amount_stage_50 = fields.Integer(string="Revenue - qualif")
    amount_stage_80 = fields.Integer(string="Revenue - Accord verbal")
    amount_stage_100 = fields.Integer(string="Revenue - Gagné")
    laststage_id = fields.Many2one('crm.stage', string="Dernière étape", store=True)
    stage_id = fields.Many2one('crm.stage', string="Etape")
    parent_id = fields.Many2one('res.partner', string="Groupe client")
    user_id = fields.Many2one('res.users', string="Vendeur")
    team_id = fields.Many2one('crm.team', string='Equipe commerciale')
    partner_id = fields.Many2one('res.partner', string="Client")


    def _select(self):
        select_str = """
        SELECT
            c.id,
            c.date_closed AS date_closed,
            c.axe1 AS axe1,
            c.axe2 AS axe2,
            c.axe3 AS axe3,
            c.axe4 AS axe4,
            c.axe5 AS axe5,
            c.stage_10 AS stage_10,
            c.stage_25 AS stage_25,
            c.stage_50 AS stage_50,
            c.stage_80 AS stage_80,
            c.stage_100 AS stage_100,
            c.stage_all AS stage_all,
            c.company_id AS company_id,
            c.amount_stage_10 AS amount_stage_10,
            c.amount_stage_25 AS amount_stage_25,
            c.amount_stage_80 AS amount_stage_80,
            c.amount_stage_50 AS amount_stage_50,
            c.amount_stage_100 AS amount_stage_100,
            c.laststage_id AS laststage_id,
            c.stage_id AS stage_id,
            c.parent_id AS parent_id,
            c.team_id AS team_id,
            c.user_id AS user_id,
            c.partner_id AS partner_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
                    "crm_lead" c
        """
        return from_str

    def _join(self):
        join_str = """
            LEFT JOIN "crm_stage" stage ON stage.id = c.stage_id
        """
        return join_str

    def _where(self):
        where_str = """
         WHERE
                c.type = 'opportunity' AND c.active = True

        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY c.id,
            date_closed,
            axe1,
            axe2,
            axe3,
            axe4,
            axe5,
            stage_10,
            stage_25,
            stage_50,
            stage_80,
            stage_100,
            stage_all,
            company_id,
            amount_stage_10,
            amount_stage_25,
            amount_stage_80,
            amount_stage_50,
            amount_stage_100,
            laststage_id,
            stage_id,
            parent_id,
            team_id,
            user_id,
            partner_id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE VIEW %s AS (
            %s
            %s
            %s
            %s
        )""" % (self._table, self._select(), self._from(), self._where(), self._group_by()))

