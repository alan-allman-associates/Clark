# -*- coding: utf-8 -*-
{
    'name': 'AAA Speed',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Speed',
    'sequence': 15,
    'description': """
AAA Speed
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['aaa_security',
                'aaa_base',
        ],
    'data': [
            'security/ir.model.access.csv',
            'views/res_partner_view.xml',
            'views/calendar_view.xml',
            'views/speed.xml',
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
