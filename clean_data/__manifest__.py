# -*- coding: utf-8 -*-
{
    'name': "Mass Clean Data (Clear Data)",
    'summary': 'This module allows to user clear the unwanted data using wizard',
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
    'description': "User can easily clean the data",
    'category': 'Tools',
    'version': '17.0',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
       'security/ir.model.access.csv',
       'wizards/clean_data_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
