# -*- coding: utf-8 -*-
{
    'name': 'AAA Hr Recruitment',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA HR Recruitment',
    'sequence': 15,
    'description': """
AAA HR Recruitment
    """,
    'category': 'Human Resources',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': [
                'crm',
                'hr_recruitment',
                'hr_contract',
                'project'
        ],
    'data': [
            'views/hr_recruitment_view.xml',
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
