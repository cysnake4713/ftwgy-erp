# coding=utf-8
__author__ = 'cysnake4713'
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

    def do_delegate(self, cr, uid, ids, delegate_data=None, context=None):
        """
        Delegate Task to another users.
        """
        if delegate_data is None:
            delegate_data = {}
        assert delegate_data['user_id'], _("Delegated User should be specified")
        delegated_tasks = {}
        for task in self.browse(cr, uid, ids, context=context):
            delegated_task_id = self.copy(cr, uid, task.id, {
                'name': delegate_data['name'],
                'project_id': delegate_data['project_id'] and delegate_data['project_id'][0] or False,
                'stage_id': delegate_data.get('stage_id') and delegate_data.get('stage_id')[0] or False,
                'user_id': delegate_data['user_id'] and delegate_data['user_id'][0] or False,
                'planned_hours': delegate_data['planned_hours'] or 0.0,
                'parent_ids': [(6, 0, [task.id])],
                'description': delegate_data['new_task_description'] or '',
                'child_ids': [],
                'work_ids': [],
                'department_id': delegate_data['department_id'] and delegate_data['department_id'][0] or False,
                'date_deadline': delegate_data['date_deadline'] and delegate_data['date_deadline'] or False,
                'date_start': delegate_data['date_start'] and delegate_data['date_start'] or False,
                'date_end': delegate_data['date_end'] and delegate_data['date_end'] or False,
            }, context=context)
            self._delegate_task_attachments(cr, uid, task.id, delegated_task_id, context=context)
            newname = delegate_data['prefix'] or ''
            task.write({
                'remaining_hours': delegate_data['planned_hours_me'],
                'planned_hours': delegate_data['planned_hours_me'] + (task.effective_hours or 0.0),
                'name': newname,
            })
            delegated_tasks[task.id] = delegated_task_id
        return delegated_tasks


class TaskTypeInherit(models.Model):
    _inherit = 'project.task.type'

    is_end = fields.Boolean('Is End')


class TaskDelegateInherit(models.Model):
    _inherit = 'project.task.delegate'

    department_id = fields.Many2one('hr.department', 'Department')
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    date_deadline = fields.Date('Date Deadline')

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        res = super(TaskDelegateInherit, self).default_get(cr, uid, fields, context=context)
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        if not record_id:
            return res
        task_pool = self.pool.get('project.task')
        task = task_pool.browse(cr, uid, record_id, context=context)

        if 'department_id' in fields:
            res['department_id'] = task.department_id.id
        if 'date_deadline' in fields:
            res['date_deadline'] = task.date_deadline
        if 'prefix' in fields:
            res['prefix'] = task.name
        if 'name' in fields:
            res['name'] = task.name + '-'

        return res

    _defaults = {
        'date_start': lambda *args: fields.Datetime.now()
    }