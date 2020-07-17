# -*- coding: utf-8 -*-
{
    'name': 'AAA Mail',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Mail',
    'sequence': 15,
    'description': """
AAA Mail
    """,
    'category': 'Sales',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['mail',
                ],
    'data': ['views/res_config_view.xml',
             'views/ir_mail_server_view.xml',
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
