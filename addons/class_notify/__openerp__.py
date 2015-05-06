# -*- coding: utf-8 -*-
{
    'name': 'Class Notify Module',
    'version': '0.2',
    'category': 'school',
    'complexity': "easy",
    'description': """
Class Notify""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'report', 'mail', 'odoosoft_workflow', 'odoosoft_wechat_enterprise'],
    'data': [
        'data/cron.xml',
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/report.xml',
        'report/report_timetable.xml',
        'views/timetable_view.xml',
        'views/plan_view.xml',
        'views/config_view.xml',
        'views/menu.xml',
        'views/mail_menu.xml',
        'views/templates.xml',

    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
