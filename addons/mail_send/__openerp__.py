# -*- coding: utf-8 -*-
{
    'name': 'Mail Send Plugin Module',
    'version': '0.2',
    'category': 'mail',
    'complexity': "easy",
    'description': """
Mail Send Plugin""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'mail'],
    'data': [
        'views/templates.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True,
}
