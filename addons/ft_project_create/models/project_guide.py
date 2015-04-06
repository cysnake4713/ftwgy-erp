# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _


class ProjectGuide(models.Model):
    _name = 'project.project.create.guide'
    _rec_name = 'name'
    _description = 'Project Create Guide'

    _inherit = 'odoosoft.workflow.abstract'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('draft', u'项目设计'),
                              ('select_approver', u'审批流程选择'),
                              ('approver_confirm', u'审批人确认'),
                              ('finished', u'项目已启动'),
                              ('cancel', u'项目取消'), ], 'State')
    create_type = fields.Selection([('create_project', u'完成后创建项目和任务'), ('create_task', u'完成后创建任务')], 'Create Type')

    department_id = fields.Many2one('hr.department', 'Department',
                                    default=lambda self: self.env.user.department_id[0] if self.env.user.department_id else False)
    user_id = fields.Many2one('res.users', 'Manager')
    date_start = fields.Date('Date Start')
    date = fields.Date('Date End')
    date_deadline = fields.Date('Deadline')
    description = fields.Text('Description')

    plan = fields.Many2one('project.project.create.plan', 'Plan')
    tasks = fields.Many2many('project.project.create.task', 'rel_project_create_tasks', 'guide_id', 'task_id', 'Plan Tasks')

    sign_template = fields.Many2one('project.project.create.sign', 'Sign Template')
    sign_group = fields.One2many('project.project.create.sign.group', 'guide_id', 'Sign Group')

    project_id = fields.Many2one('project.project', 'Relative Project')
    task_id = fields.Many2one('project.task', 'Relative Task')

    attachments = fields.Many2many('ir.attachment', 'project_create_attachment_rel', 'create_id', 'attachment_id', 'Attachments')

    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Request Datetime')

    select_approver_user = fields.Many2one('res.users', 'Select Approver User')
    select_approver_datetime = fields.Datetime('Select Approver Datetime')

    _defaults = {
        'state': 'draft',
        'create_type': 'create_project',
        'date_start': lambda *a: fields.Date.today()

    }

    _state_field_map = {
        'draft': True,
        'select_approver': True,
    }

    @api.one
    @api.constrains('date_start', 'date')
    def _check_dates(self):
        if self.date and self.date_start:
            if self.date < self.date_start:
                raise Warning(_('End Date cannot be set before Start Date.'))

    @api.multi
    def button_change_plan(self):
        if self.plan:
            self.tasks.unlink()
            new_tasks = self.plan.tasks.copy()
            new_tasks.write({'is_template': False,
                             'date_start': fields.Datetime.now()})
            self.tasks = [(6, 0, [t.id for t in new_tasks])]
            # self.tasks = [t.id for t in new_tasks]

    @api.multi
    def button_change_sign_template(self):
        if self.sign_template:
            self.sign_group.unlink()
            for line in self.sign_template.lines:
                self.sign_group.create({'user': line.user.id, 'sequence': line.sequence, 'guide_id': self.id})

    @api.multi
    def button_draft_to_select_approver(self):
        if self.create_type == 'create_project':
            if self.tasks.filtered(lambda t: not t.user_id):
                raise exceptions.Warning(_('Task assign user is empty, please define user before apply.'))
        self.common_apply()

    @api.multi
    def button_select_approver_to_confirm(self):
        if not self.sign_group:
            raise exceptions.Warning(_('No Approver Selected, Selected approver before apply.'))
        else:
            user_ids = [g.user.id for g in self.sign_group]
            self.with_context(message_users=user_ids).common_apply()

    @api.multi
    def button_approver_sign(self):
        # sign the form
        for group in self.sign_group:
            if group.user.id == self.env.uid:
                group.result = 'signed'
                break
        else:
            raise exceptions.Warning(_('You are not in the sign group!'))
        # if everyone is signed the form
        if not self.sign_group.filtered(lambda record: record.result != 'signed'):
            if self.create_type == 'create_project':
                self.create_project()
            if self.create_type == 'create_task':
                self.create_task()
            self.common_apply()

    @api.multi
    def button_approver_reject(self):
        if self.sign_group.filtered(lambda s: s.user.id == self.env.uid):
            self.common_reject()
        else:
            raise exceptions.Warning(_('You are not in the sign group!'))

    @api.one
    def create_project(self):
        # create relative project
        project_value = self.pool['project.project.create.guide'].copy_data(self.env.cr, self.env.uid, self.id, dict(self.env.context))
        # clean value
        del (project_value['state'])
        del (project_value['create_type'])
        del (project_value['plan'])
        del (project_value['tasks'])
        del (project_value['sign_template'])
        del (project_value['project_id'])
        del (project_value['lang'])
        del (project_value['tz'])
        del (project_value['uid'])

        project = self.env['project.project'].sudo().create(project_value)
        self.project_id = project
        self.attachments.write({'res_model': 'project.project', 'res_id': project.id})
        # create relative task
        for task in self.tasks:
            task_value = self.pool['project.project.create.task'].copy_data(self.env.cr, self.env.uid, task.id, dict(self.env.context))
            task_value['project_id'] = project.id
            # clear task value
            del (task_value['is_template'])
            del (task_value['lang'])
            del (task_value['tz'])
            del (task_value['uid'])
            self.env['project.task'].sudo().create(task_value)

    @api.one
    def create_task(self):
        # create relative project
        task = self.env['project.task'].sudo().create({
            'name': self.name,
            'department_id': self.department_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'date_start': self.date_start,
            'date_end': self.date,
            'date_deadline': self.date_deadline,
        })
        self.task_id = task
        self.attachments.write({'res_model': 'project.task', 'res_id': task.id})