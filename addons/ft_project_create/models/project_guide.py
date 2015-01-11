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

    plan = fields.Many2one('project.project.create.plan', 'Plan')
    tasks = fields.Many2many('project.project.create.task', 'rel_project_create_tasks', 'guide_id', 'task_id', 'Plan Tasks')

    sign_template = fields.Many2one('project.project.create.sign', 'Sign Template')
    sign_group = fields.One2many('project.project.create.sign.group', 'guide_id', 'Sign Group')

    _defaults = {
        'state': 'draft',
        'is_create_project': True,

    }

    @api.multi
    def onchange_plan(self):
        if self.plan:
            self.tasks.unlink()
            new_tasks = self.plan.tasks.copy()
            new_tasks.write({'is_template': False,
                             'date_start': fields.Date.today()})
            self.tasks = [(6, 0, [t.id for t in new_tasks])]
            # self.tasks = [t.id for t in new_tasks]

    @api.multi
    def onchange_sign_template(self):
        if self.sign_template:
            self.sign_group.unlink()
            for user in self.sign_template.users:
                self.sign_group.create({'user': user.id, 'guide_id': self.id})