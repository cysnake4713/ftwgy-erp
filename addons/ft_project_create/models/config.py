__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class TaskPlan(models.Model):
    _name = 'project.project.create.plan'

    name = fields.Char('Name', required=True)
    tasks = fields.Many2many('project.project.create.task', 'rel_project_create_plan_tasks', 'plan_id', 'task_id', 'Plan Tasks')


class TaskLine(models.Model):
    _name = 'project.project.create.task'

    name = fields.Char('Name', required=True)
    department_id = fields.Many2one('hr.department', 'Department')
    user_id = fields.Many2one('res.users', 'In Charge User', required=True)
    reviewer_id = fields.Many2one('res.users', 'Reviewer')
    description = fields.Text('Description')
    date_deadline = fields.Date('Deadline')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date End')
    categ_ids = fields.Many2many('project.category', 'rel_project_create_task_category', 'task_id', 'category_id', 'Categories')
    is_template = fields.Boolean('Is Template')

    _defaults = {
        'date_start': lambda *a: fields.Date.today()
    }


class SignTemplate(models.Model):
    _name = 'project.project.create.sign'

    name = fields.Char('Name', required=True)
    users = fields.Many2many('res.users', 'project_create_sign_user', 'sign_id', 'user_id', 'Users')


class SignUser(models.Model):
    _name = 'project.project.create.sign.group'
    _order = 'sequence'
    _rec_name = 'user'

    sequence = fields.Integer('Index')
    user = fields.Many2one('res.users', 'User', required=True)
    result = fields.Selection([('wait', u'待签'),
                               ('signed', u'已签'),
                               ('deny', u'否决'),
                               # ('reject', u'打回'),
                              ], 'Sign Result')
    guide_id = fields.Many2one('project.project.create.guide', 'Project Guide', ondelete='cascade')

    _defaults = {
        'sequence': 1,
        'result': 'wait',
    }
