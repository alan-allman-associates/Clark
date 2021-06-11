# -*- coding: utf-8 -*-
{
    'name': 'AAA Contact',
    'installed_version': '12.0.1.1',
    'version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Contact',
    'sequence': 15,
    'description': """
AAA Calendar
    """,
    'category': 'Extra Tools',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': [
               'base',
               'calendar',
                'crm',
        ],
    'data': [
        'data/scheduler.xml',
        'data/mail_template.xml',
        'data/ir_config_parameter.xml',
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
