# -*- coding: utf-8 -*-
{
    'name': 'Project Create Guide Module',
    'version': '0.2',
    'category': 'project_create',
    'complexity': "easy",
    'description': """
Project Create Guide Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'ft_project', 'odoosoft_workflow', 'odoosoft_wechat_enterprise'],
    'data': [
        'data/data.xml',
        'security/security.xml',
        'views/create_config_view.xml',
        'views/create_guide_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True,
}
