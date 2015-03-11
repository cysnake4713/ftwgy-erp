__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class DocumentTransform(models.Model):
    _name = 'ft.document.transform'
    _inherit = ['mail.thread', 'odoosoft.workflow.abstract']
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('principal', 'Principal'),
                              ('department', 'Department'),
                              ('finish', 'Finish'), ], 'State', default='draft', track_visibility='onchange')
    # draft
    attachments = fields.Many2many('ir.attachment', 'rel_ft_doc_attachments', 'doc_id', 'attachment_id', 'Attachments')
    request_principal_user = fields.Many2one('res.users', 'Request Principal User')
    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Request Datetime')
    # principal
    request_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_department_users', 'doc_id', 'user_id', 'Request Department Users')
    principal_user = fields.Many2one('res.users', 'Principal User')
    principal_datetime = fields.Datetime('Principal Datetime')
    # department
    department_comment = fields.Text('Department Comment')
    department_comment_user = fields.Many2many('res.users', 'rel_ft_doc_trans_comment_users', 'doc_id', 'user_id', 'Department Comment User')
    department_user = fields.Many2one('res.users', 'Department User')
    department_datetime = fields.Datetime('Department Datetime')

    comment = fields.Text('Comment')

    _state_field_map = {
        'draft': True,
        'principal': {
            'user': ['principal_user'],
            'time': ['principal_datetime'],
        },
        'department': {
            'user': ['department_user'],
            'time': ['department_datetime'],
        },
        'finish': False,

    }







