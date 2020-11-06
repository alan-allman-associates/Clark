# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)



class ResPartner(models.Model):
    _inherit = 'res.partner'

    def partner_deactivate(self):
        _logger.info('Scheduler is running to deactivate partner with name with @')
        nowDatetime = datetime.now()
        partners = self.env['res.partner'].search([('name','like','%@%'),('active','=', True)])
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
                    partner.active = False
                    _logger.info('Contact desactive: {}'.format(partner.name))
        _logger.info('Contact Scheduler: Successfully deactivate partner')
