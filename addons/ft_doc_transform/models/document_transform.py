__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class DocumentTransform(models.Model):
    _name = 'ft.document.transform'
    _inherit = ['mail.thread', 'odoosoft.workflow.abstract']
    _rec_name = 'name'
    _description = 'FT Doc Transform'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('principal', 'Principal'),
                              ('department', 'Department'),
                              ('finish', 'Finish'), ('finish_teacher', 'Finish By Teacher')], 'State', default='draft', track_visibility='onchange')
    # draft
    attachments = fields.Many2many('ir.attachment', 'rel_ft_doc_attachments', 'doc_id', 'attachment_id', 'Attachments')
    request_principal_user = fields.Many2one('res.users', 'Request Principal User')
    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Request Datetime')
    # principal
    principal_apply_type = fields.Selection([('department', 'To Department'), ('teacher', 'To Teacher')], 'Principal To', default='department')
    request_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_department_users', 'doc_id', 'user_id', 'Request Department Users')
    request_department_teacher_users = fields.Many2many('res.users', 'rel_ft_doc_trans_cc_users', 'doc_id', 'user_id', 'Request Department CC Users')
    principal_user = fields.Many2one('res.users', 'Principal User')
    principal_datetime = fields.Datetime('Principal Datetime')
    # department
    department_comment = fields.Text('Department Comment')
    department_comment_user = fields.Many2many('res.users', 'rel_ft_doc_trans_comment_users', 'doc_id', 'user_id', 'Department Comment User')
    department_user = fields.Many2one('res.users', 'Department User')
    department_datetime = fields.Datetime('Department Datetime')

    comment = fields.Html('Comment')

    _state_field_map = {
        'draft': True,
        'principal': {
            'user': ['principal_user'],
            'time': ['principal_datetime'],
        },
        'department': True,
        'finish': False,
    }

    @api.multi
    def principal_apply(self):
        if self.principal_apply_type == 'teacher':
            local_context = self.env.context.copy()
            local_context.update({'state': 'finish_teacher'})
            return self.with_context(local_context).common_apply()
        else:
            return self.common_apply()







