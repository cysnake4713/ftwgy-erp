# -*- coding: utf-8 -*-
{
    'name': ' FTWGY Wen Jian Liu Zhuan',
    'version': '0.2',
    'category': 'wenjianliuzhuan',
    'complexity': "easy",
    'description': """
""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'mail', 'odoosoft_workflow'],
    'data': [
        'security/security.xml',

        'views/menu.xml',
        'views/doc_transform_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}