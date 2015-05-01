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
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('principal', 'Principal'),
                              ('vice_principal', 'Vice Principal'),
                              ('department', 'Department'),
                              ('finish', 'Finish'), ('finish_teacher', 'Finish By Teacher')], 'State', default='draft', track_visibility='onchange')
    # draft
    attachments = fields.Many2many('ir.attachment', 'rel_ft_doc_attachments', 'doc_id', 'attachment_id', 'Attachments')
    request_principal_user = fields.Many2one('res.users', 'Request Principal User')
    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Request Datetime')
    from_unit = fields.Char('From Unit')
    code = fields.Char('Code')
    receive_date = fields.Date('Receive Date', default=lambda *o: fields.Date.today())
    urgency = fields.Selection([('normal', u'一般'),
                                ('urgent', u'紧急'),
                                ('very_urgent', u'加急')], 'Urgency', default='normal')
    # principal
    principal_apply_type = fields.Selection([('vice_principal', 'To Vice Principal'), ('department', 'To Department'), ('teacher', 'To Teacher')],
                                            'Principal To', default='vice_principal')
    request_principal_vice_principal = fields.Many2one('res.users', 'Request Vice Principal User')
    request_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_department_users', 'doc_id', 'user_id', 'Request Department Users')
    request_department_teacher_users = fields.Many2many('res.users', 'rel_ft_doc_trans_cc_users', 'doc_id', 'user_id', 'Request Department CC Users')
    principal_user = fields.Many2one('res.users', 'Principal User')
    principal_datetime = fields.Datetime('Principal Datetime')
    principal_comment = fields.Text('Principal Comment')
    # vice_principal
    vice_principal_apply_type = fields.Selection([('department', 'To Department'), ('teacher', 'To Teacher')], 'Vice Principal To',
                                                 default='department')
    request_vice_department_teacher_users = fields.Many2many('res.users', 'rel_ft_doc_trans_vice_cc_users', 'doc_id', 'user_id',
                                                             'Vice Request Teacher')
    request_vice_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_vice_department_users', 'doc_id', 'user_id',
                                                     'Vice Request Department Users')
    vice_principal_user = fields.Many2one('res.users', 'Vice Principal User')
    vice_principal_datetime = fields.Datetime('Vice Principal Datetime')
    vice_principal_comment = fields.Text('Vice Principal Comment')
    # department
    department_comment = fields.Text('Department Comment')
    department_comment_user = fields.Many2many('res.users', 'rel_ft_doc_trans_comment_users', 'doc_id', 'user_id', 'Department Comment User')
    department_user = fields.Many2one('res.users', 'Department User')
    department_datetime = fields.Datetime('Department Datetime')

    comment = fields.Html('Comment')

    results = fields.One2many('ft.document.transform.result', 'transform', 'Results')

    _state_field_map = {
        'draft': True,
        'principal': True,
        'vice_principal': True,
        'department': True,
        'finish': False,
    }

    @api.multi
    def button_draft(self):
        if self.sudo(self.request_principal_user.id).user_has_groups('ft_doc_transform.group_doc_trans_vice_principal'):
            return self.with_context(state='vice_principal').common_apply()
        return self.common_apply()

    @api.multi
    def principal_apply(self):
        if self.principal_apply_type == 'vice_principal':
            return self.with_context(state='vice_principal', message_users=[self.request_principal_vice_principal.id]).common_apply()
        elif self.principal_apply_type == 'department':
            return self.with_context(state='department').common_apply()
        else:
            self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.request_department_teacher_users]})
            return self.common_apply()

    @api.multi
    def vice_principal_apply(self):
        if self.vice_principal_apply_type == 'department':
            return self.with_context(state='department').common_apply()
        elif self.vice_principal_apply_type == 'teacher':
            self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.request_vice_department_teacher_users]})
            return self.with_context(state='finish').common_apply()
        else:
            return self.common_apply()

    @api.multi
    def vice_principal_reject(self):
        if self.principal_user:
            return self.with_context(state='principal', message_users=[self.request_principal_user.id]).common_apply()
        else:
            return self.common_apply()

    @api.multi
    def button_department_finish(self):
        self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.department_comment_user]})
        self.common_apply()

    @api.multi
    def button_teacher_finish(self):
        results = self.results.filtered(lambda result: result.user.id == self.env.uid)
        results.write({
            'finish_date': fields.Datetime.now(),
            'state': 'finished',
        })


class UserResult(models.Model):
    _name = 'ft.document.transform.result'
    _description = 'Doc Transform Result'
    _rec_name = 'user'

    transform = fields.Many2one('ft.document.transform', 'Related Transform', ondelete='cascade')
    user = fields.Many2one('res.users', 'User')
    finish_date = fields.Datetime('Finished Time')
    state = fields.Selection([('processing', u'处理中'), ('finished', u'完成')], 'State', default='processing')







