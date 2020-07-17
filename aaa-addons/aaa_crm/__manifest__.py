# -*- coding: utf-8 -*-
{
    'name': 'AAA CRM',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA CRM',
    'sequence': 15,
    'description': """
AAA CRM
    """,
    'category': 'Sales',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['sales_team',
                'crm',
                'aaa_security',
                ],
    'data': ['security/ir.model.access.csv',
             'views/crm_lead_view.xml',
             'views/crm_team_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': '',
}
