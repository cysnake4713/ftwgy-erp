# -*- coding: utf-8 -*-
{
    'name': 'Class Nofity Module',
    'version': '0.2',
    'category': 'school',
    'complexity': "easy",
    'description': """
Class Nofity""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'report'],
    'data': [
        'report/report.xml',
        'report/report_timetable.xml',
        'views/timetable_view.xml',
        'views/plan_view.xml',
        'views/config_view.xml',
        'views/menu.xml',
        'views/mail_menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
