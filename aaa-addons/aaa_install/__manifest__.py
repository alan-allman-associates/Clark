# -*- coding: utf-8 -*-
{
    'name': 'AAA Install',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Install',
    'sequence': 15,
    'description': """
Install AAA modules
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['aaa_speed',
                'aaa_project',
                'aaa_calendar',
                'aaa_crm',
                'aaa_hr',
                'aaa_hr_recruitment',
                'aaa_hr_skill',
                'aaa_simus',
                'aaa_alarms',
                'aaa_sale',
                ],
    'data': [
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
