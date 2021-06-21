# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)



class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    archive_script = fields.Boolean(string="Archive avec le script")

    def log(self, message, level="info"):
        with self.pool.cursor() as cr:
            cr.execute("""
                INSERT INTO ir_logging(create_date, create_uid, type, dbname, name, level, message, path, line, func)
                VALUES (NOW() at time zone 'UTC', %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.env.uid, 'server', self._cr.dbname, __name__, level, message, "action", self.id, self.name))

    def partner_deactivate(self):
        partners_deactivate = self.env['res.partner']
        _logger.info('Scheduler is running to deactivate partner with name with @')
        nowDatetime = datetime.now()
        partners = self.env['res.partner'].search(
            ['&',
             '&',
             '&',
             ('email', '!=', 'admin'),
             ('is_company', '=', False),
             ('active', '=', True),
             '|',
             ('parent_id', '=', False),
             ('parent_id.active', '=', False),
             '|',
             ('name', 'not like', '[%'),
             '|',
             ('name', 'not like', '%]%'),
             ('name', 'like', '%@%')], limit=40)
        partners and partners[0].log("Nbre de contact est %s" %(len(partners)))
        partners and partners[0].log("Les contacts sont %s" %(partners.mapped('name')))
        for partner in partners:
            deactive = True
            attendees = self.env['calendar.attendee'].search([('partner_id','=', partner.id)])
            if attendees:
                for attendee in attendees:
                    events = self.env['calendar.event'].search([('id','=', attendee.event_id.id)])
                    if events:
                        for event in events:
                            if event.start > nowDatetime:
                                deactive = False
                if deactive:
                    partners_deactivate.archive_script = True
                    partners_deactivate += partner
                    _logger.info('Contact desactive: {}'.format(partner.name))
        template = self.env.ref('aaa_contact.partner_active_false', raise_if_not_found=False)
        if partners_deactivate:
            partner_to = self.env['ir.config_parameter'].sudo().get_param('partner_to.send_deactivate_partner')
            email_from = self.env['ir.config_parameter'].sudo().get_param('email_from.send_deactivate_partner')
            partners_deactivate.write({'active': False})
            if template and partner_to and email_from:
                template.with_context(partner_to=int(partner_to), email_from = email_from, partner_ids = partners_deactivate.ids).send_mail(self.id, email_values={'subject' : "La liste des contacts archivés", })
                _logger.info('Contact Scheduler: Successfully deactivate partner')

