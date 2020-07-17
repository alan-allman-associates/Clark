# -*- coding: utf-8 -*-
{
    'name': 'AAA Hr',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA HR',
    'sequence': 15,
    'description': """
AAA HR
    """,
    'category': 'Human Resources',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['hr',
                'hr_timesheet',
                'hr_contract',
                #'hr_holidays',
                'aaa_base',
                'aaa_security',
    ],
    'data': ['security/ir_rule.xml',
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
