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
        'views/project_view.xml',
        'views/task_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
