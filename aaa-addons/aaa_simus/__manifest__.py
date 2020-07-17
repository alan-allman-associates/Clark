# -*- coding: utf-8 -*-
{
    'name': 'AAA Simus',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Simus',
    'sequence': 15,
    'description': """
AAA Simus
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': [
                'base',
                'aaa_base',
                'aaa_hr',
                'aaa_project',
                'aaa_mail',
#                 'aaa_employee_firstname',
        ],
    'data': [
            'data/ir_cron.xml',
            'data/ir_config_parameter.xml',
            #'views/res_company.xml',
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
