# -*- coding: utf-8 -*-
{
    'name': 'FTWGY Department Module',
    'version': '0.2',
    'category': 'base',
    'complexity': "easy",
    'description': """
FTWGY Department """,
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base'],
    'data': [
        'views/department_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
