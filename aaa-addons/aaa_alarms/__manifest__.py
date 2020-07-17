# -*- coding: utf-8 -*-
{
    'name': 'AAA Alarms',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Alarms',
    'sequence': 15,
    'description': """
AAA Alarms
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['project',
                'aaa_hr',
                'aaa_security',
                ],
    'data': ['data/calendar_alarm.xml',
             'data/ir_cron.xml',
             'data/ir_config_parameter.xml',
             'views/res_company_view.xml',
             'views/hr_view.xml',
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
