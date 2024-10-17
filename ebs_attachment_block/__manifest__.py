# -*- coding: utf-8 -*-
{
    'name': "Block attachments",

    'summary': 'Block attachments',

    'description': """
        Block attachments
    """,

    'author': "jaafar khansa",
    'website': "http://www.ever-bs.com/",
    'category': 'Administration',
    'version': '17.0',
    'installable': True,
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
        'views/attachment_block.xml',

    ],
}
