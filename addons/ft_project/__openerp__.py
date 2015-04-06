# -*- coding: utf-8 -*-
{
    'name': 'FTWGY Project Module',
    'version': '0.2',
    'category': 'project',
    'complexity': "easy",
    'description': """
FTWGY Project Module """,
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'project', 'ft_department'],
    'data': [
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/task_view.xml',
        'views/menu.xml',
        'views/mail_menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
