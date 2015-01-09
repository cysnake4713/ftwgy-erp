__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectGuide(models.Model):
    _name = 'project.project.create.guide'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('draft', u'项目设计'),
                              ('select_approver', u'审批流程选择'),
                              ('approver_confirm', u'审批人确认'),
                              ('finished', u'项目启动'),
                              ('cancel', u'项目取消'), ], 'State')
    is_create_project = fields.Boolean('Is Create Project')
    description = fields.Text('Description')

    plan_id = fields.Many2one('project.project.plan', 'Plan')
    task_ids = fields.Many2many('project.project.plan.task', 'rel_project_task', 'guide_id', 'task_id', 'Plan Tasks')

    _defaults = {
        'state': 'draft',
        'is_create_project': True,

    }


class TaskPlan(models.Model):
    _name = 'project.project.plan'

    name = fields.Char('Name', required=True)
    tasks = fields.Many2many('project.project.plan.task', 'rel_plan_line', 'plan_id', 'task_id', 'Plan Tasks')


class TaskLine(models.Model):
    _name = 'project.project.plan.task'

    name = fields.Char('Name', required=True)
    department_id = fields.Many2one('hr.department', 'Department')
    user_id = fields.Many2one('res.users', 'In Charge User', required=True)
    reviewer_id = fields.Many2one('res.users', 'Reviewer')
    description = fields.Text('Description')
    date_deadline = fields.Date('Deadline')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date End')
    categ_ids = fields.Many2many('project.category', 'rel_plan_task_category', 'task_id', 'category_id', 'Categories')

    _defaults = {
        'date_start': lambda *a: fields.Date.today()
    }