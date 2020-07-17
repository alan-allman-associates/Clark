# -*- coding: utf-8 -*-
{
    'name': 'AAA Project',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA Project',
    'sequence': 15,
    'description': """
AAA Project
    """,
    'category': 'Project',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': ['crm',
                'project',
        ],
    'data': ['views/project_view.xml',
             'views/task_view.xml',
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
