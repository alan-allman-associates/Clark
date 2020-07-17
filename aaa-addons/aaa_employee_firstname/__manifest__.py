# -*- coding: utf-8 -*-

{
    'name': 'AAA Employee first name and last name',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'Split first name and last name for employees and partners addresses associated',
    'sequence': 15,
    'description': """
Split first name and last name for employees and addresses
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['hr',
                ],
    'data': ['views/base_config_view.xml',
             'views/res_partner_view.xml',
             'views/res_users_view.xml',
             'views/hr_view.xml',
             'views/resource_view.xml',
             ],
    'demo': [
    ],
    'qweb': [
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
