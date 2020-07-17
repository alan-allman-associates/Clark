# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    Part of Odoo. See LICENSE file for full copyright and licensing details.   #
#    Copyright (C) 2018 Jupical Technologies Pvt. Ltd. <http://www.jupical.com> #
#                                                                               #
#################################################################################

{
    'name': 'SMTP BY USER OR COMPANY',
    'description':"""Customised module which allows to configure
            outgoing email server by user or company.
                """,
    'version': '12.0.0.1.0',
    'category': 'Mail',
    'author': 'Jupical Technologies Pvt. Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'website': 'https://www.jupical.com',
    'depends': ['mail'],
    'summary':"""Configure different outgoing mail server for each company or
        each user
    """,
    'license': 'AGPL-3',
    'data': [
        'views/res_config_views.xml',
        'views/ir_mail_server_view.xml',
             ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'images':['static/description/poster_image.png'],
    'price': 30.00,
    'currency': 'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: