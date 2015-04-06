# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class TaskPlan(models.Model):
    _name = 'project.project.create.plan'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    tasks = fields.Many2many('project.project.create.task', 'rel_project_create_plan_tasks', 'plan_id', 'task_id', 'Plan Tasks')


class TaskLine(models.Model):
    _name = 'project.project.create.task'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    department_id = fields.Many2one('hr.department', 'Department',
                                    default=lambda self: self.env.user.department_id[0] if self.env.user.department_id else False)
    user_id = fields.Many2one('res.users', 'In Charge User')
    reviewer_id = fields.Many2one('res.users', 'Reviewer')
    description = fields.Text('Description')
    date_deadline = fields.Date('Deadline')
    date_start = fields.Datetime('Date start')
    date_end = fields.Datetime('Date End')
    categ_ids = fields.Many2many('project.category', 'rel_project_create_task_category', 'task_id', 'category_id', 'Categories')
    is_template = fields.Boolean('Is Template')

    _defaults = {
        'date_start': lambda *a: fields.Datetime.now()
    }


class SignTemplate(models.Model):
    _name = 'project.project.create.sign'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    lines = fields.One2many('project.project.create.sign.line', 'sign_id', 'Sign Users Lines')


class SignTemplateLine(models.Model):
    _name = 'project.project.create.sign.line'
    _rec_name = 'user'

    sign_id = fields.Many2one('project.project.create.sign', 'Sign', ondelete='cascade')
    sequence = fields.Integer('Index', default=1)
    user = fields.Many2one('res.users', 'User', required=True)


class SignUser(models.Model):
    _name = 'project.project.create.sign.group'
    _order = 'sequence'
    _rec_name = 'user'

    sequence = fields.Integer('Index')
    user = fields.Many2one('res.users', 'User', required=True)
    result = fields.Selection([('wait', u'待签'),
                               ('signed', u'已签'),
                               ('deny', u'否决')], 'Sign Result')
    guide_id = fields.Many2one('project.project.create.guide', 'Project Guide', ondelete='cascade')

    _defaults = {
        'sequence': 1,
        'result': 'wait',
    }
