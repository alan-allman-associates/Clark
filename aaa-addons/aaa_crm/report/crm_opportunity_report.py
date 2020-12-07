# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api

from odoo.addons.crm.models import crm_stage

class OpportunityReport(models.Model):
    """ CRM Opportunity Analysis """

    _name = "crm.opportunity.report"
    _auto = False
    _description = "CRM Opportunity Analysis"
    _rec_name = 'date_deadline'

    date_deadline = fields.Date('Expected Closing', readonly=True)
    create_date = fields.Datetime('Creation Date', readonly=True)
    opening_date = fields.Datetime('Assignation Date', readonly=True)
    date_closed = fields.Datetime('Close Date', readonly=True)
    date_last_stage_update = fields.Datetime('Last Stage Update', readonly=True)
    active = fields.Boolean('Active', readonly=True)

    # durations
    delay_open = fields.Float('Delay to Assign', digits=(16, 2), readonly=True, group_operator="avg", help="Number of Days to open the case")
    delay_close = fields.Float('Delay to Close', digits=(16, 2), readonly=True, group_operator="avg", help="Number of Days to close the case")
    delay_expected = fields.Float('Overpassed Deadline', digits=(16, 2), readonly=True, group_operator="avg")

    user_id = fields.Many2one('res.users', string='User', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Channel', oldname='section_id', readonly=True)
    nbr_activities = fields.Integer('# of Activities', readonly=True)
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country', readonly=True)
    probability = fields.Float(string='Probability', digits=(16, 2), readonly=True, group_operator="avg")
    total_revenue = fields.Float(string='Total Revenue', digits=(16, 2), readonly=True)
    expected_revenue = fields.Float(string='Probable Turnover', digits=(16, 2), readonly=True)
    stage_id = fields.Many2one('crm.stage', string='Stage', readonly=True, domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]")
    stage_name = fields.Char(string='Stage Name', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    priority = fields.Selection(crm_stage.AVAILABLE_PRIORITIES, string='Priority', group_operator="avg")
    type = fields.Selection([
        ('lead', 'Lead'),
        ('opportunity', 'Opportunity'),
    ], help="Type is used to separate Leads and Opportunities")
    lost_reason = fields.Many2one('crm.lost.reason', string='Lost Reason', readonly=True)
    date_conversion = fields.Datetime(string='Conversion Date', readonly=True)
    campaign_id = fields.Many2one('utm.campaign', string='Campaign', readonly=True)
    source_id = fields.Many2one('utm.source', string='Source', readonly=True)
    medium_id = fields.Many2one('utm.medium', string='Medium', readonly=True)
    closing_rate = fields.Float(string='Taux de closing', digits=(16, 2), readonly=True)
    conversion_rate = fields.Float(string='Taux de transformation', digits=(16, 2), readonly=True)
    overall_efficiency_rate = fields.Float(string="Taux d'efficacité globale", digits=(16, 2), readonly=True)
    portfolio_maturity = fields.Float(string="Maturité protefeuille", digits=(16, 2), readonly=True)



    def get_short_id(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('short_list_stage_id'))

    def get_win_stage_id(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('gagne_stage_id'))

    def get_proposal_stage_id(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('proposition_stage_id'))

    def get_qualified_stage_id(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('qualified_stage_id'))




    def _select(self):
        select_str = """
        SELECT
            c.id,
            c.date_deadline,
            c.date_open as opening_date,
            c.date_closed as date_closed,
            c.date_last_stage_update as date_last_stage_update,
            c.user_id,
            c.probability,
            c.stage_id,
            stage.name as stage_name,
            c.type,
            c.company_id,
            c.priority,
            c.team_id,
            (SELECT COUNT(*)
             FROM mail_message m
             WHERE m.model = 'crm.lead' and m.res_id = c.id) as nbr_activities,
            (SELECT (COUNT(c.id) / CASE COALESCE(short.total_short, 0) WHEN 0 THEN 1.0 ELSE short.total_short END) FROM crm_lead lead ,(SELECT COUNT(l.id) total_short FROM crm_lead l where l.stage_id = %d and c.company_id = l.company_id AND l.active = c.active and l.type = c.type) short where lead.id=c.id and lead.stage_id = %d) as closing_rate,
            (SELECT (COUNT(c.id) / CASE COALESCE(conversion.total_conversion, 0) WHEN 0 THEN 1.0 ELSE conversion.total_conversion END) FROM crm_lead lead, (SELECT COUNT(l.id) total_conversion FROM crm_lead l where l.stage_id = %d and c.company_id = l.company_id AND l.active = c.active and l.type = c.type) conversion  where lead.id=c.id and lead.stage_id = %d) as conversion_rate,
            (SELECT (COUNT(c.id) / CASE COALESCE(overall_efficiency.total_overall_efficiency, 0) WHEN 0 THEN 1.0 ELSE overall_efficiency.total_overall_efficiency END) FROM crm_lead lead, (SELECT COUNT(l.id) total_overall_efficiency FROM crm_lead l where l.stage_id = %d and c.company_id = l.company_id AND l.active = c.active and l.type = c.type) overall_efficiency where lead.id=c.id and lead.stage_id = %d) as overall_efficiency_rate,
            (SELECT ((c.planned_revenue * stage.probability / 100.0) / total.total_lead) FROM crm_lead lead , (SELECT COUNT(l.id) total_lead FROM crm_lead l where c.company_id = l.company_id AND l.active = c.active and l.type = c.type) total,
            crm_stage stage WHERE c.id = lead.id and lead.stage_id = stage.id) as portfolio_maturity,
            c.active,
            c.campaign_id,
            c.source_id,
            c.medium_id,
            c.partner_id,
            c.city,
            c.country_id,
            c.planned_revenue as total_revenue,
            c.planned_revenue*(c.probability/100) as expected_revenue,
            c.create_date as create_date,
            extract('epoch' from (c.date_closed-c.create_date))/(3600*24) as  delay_close,
            abs(extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24)) as  delay_expected,
            extract('epoch' from (c.date_open-c.create_date))/(3600*24) as  delay_open,
            c.lost_reason,
            c.date_conversion as date_conversion
        """%(self.get_short_id(), self.get_win_stage_id(), self.get_proposal_stage_id(), self.get_win_stage_id(), self.get_qualified_stage_id(), self.get_win_stage_id())
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
            GROUP BY c.id, stage.name

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
            %s
        )""" % (self._table, self._select(), self._from(), self._join(), self._where(), self._group_by()))
