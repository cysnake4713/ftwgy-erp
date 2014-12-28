# -*- coding: utf-8 -*-
{
    'name': 'School Class Import Module',
    'version': '0.2',
    'category': 'updis',
    'complexity': "easy",
    'description': """
School Class Import""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'class_notify', 'base_import'],
    # 'depends': ['base',],
    'data': [
        'views/import_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
