# -*- coding: utf-8 -*-
{
    'name': 'AAA Contact',
    'installed_version': '12.0.1.1',
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
        ],
    'data': [
        'data/scheduler.xml',
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
