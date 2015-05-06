# -*- coding: utf-8 -*-
{
    'name': 'FTWGY Mail Send Plugin Module',
    'version': '0.2',
    'category': 'mail',
    'complexity': "easy",
    'description': """
FTWGY Mail Send Plugin Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'mail', 'odoosoft_mail_send', 'ft_department'],
    'data': [
        'views/compose_view.xml',
        # 'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True,
}
