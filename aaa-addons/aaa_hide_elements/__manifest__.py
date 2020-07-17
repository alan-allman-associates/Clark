# -*- coding: utf-8 -*-
{
    'name': 'AAA Hide Elements',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Hide Elements',
    'sequence': 15,
    'description': """
AAA Hide Elements
    """,
    'category': 'Sales',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['hr_holidays',
                'hr_expense',
                'hr_recruitment',
                'mass_mailing',
                'website',
                'mail',
                ],
    'data': ['security/groups.xml',
             #'views/menu.xml',
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
