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
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/doc_transform_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
