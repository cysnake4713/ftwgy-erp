__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectInherit(models.Model):
    _inherit = 'project.project'

    department_id = fields.Many2one('hr.department', 'Department')

    task_process = fields.Float('Task Process', compute='_compute_task_process')
    description = fields.Text('Description')

    @api.multi
    @api.depends('tasks.stage_id.is_end')
    def _compute_task_process(self):
        for project in self:
            total = len(project.tasks)
            finished = len(project.tasks.filtered(lambda record: record.stage_id.is_end is True))
            project.task_process = finished / float(total) * 100 if total else 0


class Analytic(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def create(self, vals):
        rec = self.with_context({'mail_create_nolog': True})
        return super(Analytic, rec).create(vals)


class TaskInherit(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', 'Department')

    @api.multi
    def write(self, vals):
        # auto update date end
        if 'stage_id' in vals and self.env['project.task.type'].browse(vals['stage_id']).is_end is True:
            vals['date_end'] = fields.Datetime.now()
        # auto update members
        result = super(TaskInherit, self).write(vals)
        self._update_members(vals)
        return result

    @api.model
    def create(self, vals):
        result = super(TaskInherit, self).create(vals)
        result._update_members(vals)
        return result

    @api.multi
    def _update_members(self, vals):
        if ('user_id' in vals and vals['user_id']) or ('project_id' in vals and vals['project_id']):
            for task in self:
                if task.project_id:
                    task.project_id.write({'members': [(4, task.user_id.id)]})


class TaskTypeInherit(models.Model):
    _inherit = 'project.task.type'

    is_end = fields.Boolean('Is End')
