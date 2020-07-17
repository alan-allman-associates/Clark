# -*- coding: utf-8 -*-
{
    'name': 'AAA FTP SIMUS',
    'installed_version': '12.0.1.1',
    'author': 'Auguria SAS',
    'licence': 'LGPL Version 3',
    'summary': 'AAA FTP',
    'sequence': 15,
    'description': """
AAA FTP SIMUS
    """,
    'category': '',
    'website': 'https://www.auguria.fr',
    'images': [],
    'depends': [
                'base',
        ],
    'data': [
            'security/ir.model.access.csv',
            'data/res_ftp_data.xml',
            'views/res_ftp.xml',
            #'data/ir_cron.xml',
            #'data/ir_config_parameter.xml',
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
