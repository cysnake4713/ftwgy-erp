# -*- coding: utf-8 -*-
{
    'name': 'UPDIS HR Module',
    'version': '0.2',
    'category': 'updis',
    'complexity': "easy",
    'description': """
UPDIS HR """,
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'project'],
    'data': [
        'views/project_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
