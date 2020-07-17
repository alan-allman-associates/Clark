# -*- coding: utf-8 -*-
{
    'name': 'AAA Sale',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Sale',
    'sequence': 15,
    'description': """
AAA Sale
    """,
    'category': 'Sales',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['aaa_security',
                'aaa_crm',
                'sale_crm',
                ],
    'data': ['views/sale_view.xml',
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
