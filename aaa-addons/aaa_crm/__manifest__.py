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
                'sale_crm',
                'crm',
                'aaa_security',
                'mail',
                ],
    'data': ['security/ir.model.access.csv',
             'security/res_groups.xml',
             'security/ir_rule.xml',
             'data/ir_config_parameter.xml',
             'views/crm_lead_view.xml',
             'views/crm_stage.xml',
             'views/crm_team_view.xml',
             'views/mail_message_view.xml',
             'report/crm_opportunity_report_views.xml',
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
