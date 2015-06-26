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
                              ('finish_teacher', 'Finish By Teacher'),
                              ('finish', 'Finish')], 'State', default='draft', track_visibility='onchange')
    # draft
    attachments = fields.Many2many('ir.attachment', 'rel_ft_doc_attachments', 'doc_id', 'attachment_id', 'Attachments')
    comment = fields.Html('Comment')
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
    principal_apply_type = fields.Selection(
        [('vice_principal', 'To Vice Principal'), ('department', 'To Department'), ('teacher', 'To Teacher'), ('to_end', 'To End')],
        'Principal To', default='vice_principal')
    request_principal_vice_principals = fields.Many2many('res.users', 'rel_ft_doc_trans_v_principal_users', 'doc_id', 'user_id',
                                                         'Request Vice Principal Users')
    request_principal_vice_principal = fields.Many2one('res.users', 'Request Vice Principal User')
    request_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_department_users', 'doc_id', 'user_id', 'Request Department Users')
    request_department_teacher_users = fields.Many2many('res.users', 'rel_ft_doc_trans_cc_users', 'doc_id', 'user_id', 'Request Department CC Users')
    principal_user = fields.Many2one('res.users', 'Principal User')
    principal_datetime = fields.Datetime('Principal Datetime')
    principal_comment = fields.Text('Principal Comment')
    # vice_principal
    vice_principal_apply_type = fields.Selection([('department', 'To Department'), ('teacher', 'To Teacher'), ('to_end', 'To End')],
                                                 'Vice Principal To', default='department')
    request_vice_department_teacher_users = fields.Many2many('res.users', 'rel_ft_doc_trans_vice_cc_users', 'doc_id', 'user_id',
                                                             'Vice Request Teacher')
    request_vice_department_users = fields.Many2many('res.users', 'rel_ft_doc_trans_vice_department_users', 'doc_id', 'user_id',
                                                     'Vice Request Department Users')
    vice_principal_user = fields.Many2one('res.users', 'Vice Principal User')
    vice_principal_datetime = fields.Datetime('Vice Principal Datetime')
    vice_principal_comment = fields.Text('Vice Principal Comment')
    # department
    department_apply_type = fields.Selection([('teacher', 'To Teacher'), ('to_end', 'To End')], 'Department To', default='teacher')
    department_comment = fields.Text('Department Comment')
    department_comment_user = fields.Many2many('res.users', 'rel_ft_doc_trans_comment_users', 'doc_id', 'user_id', 'Department Comment User')
    department_user = fields.Many2one('res.users', 'Department User')
    department_datetime = fields.Datetime('Department Datetime')

    results = fields.One2many('ft.document.transform.result', 'transform', 'Results')

    _state_field_map = {
        'draft': True,
        'principal': True,
        'vice_principal': True,
        'department': True,
    }

    @api.multi
    def button_draft(self):
        if self.sudo(self.request_principal_user.id).user_has_groups('ft_doc_transform.group_doc_trans_vice_principal'):
            return self.with_context(state='vice_principal').common_apply()
        return self.common_apply()

    @api.multi
    def principal_apply(self):
        if self.principal_apply_type == 'vice_principal':
            self.write({'request_department_users': [(5, 0, 0)],
                        'request_department_teacher_users': [(5, 0, 0)]})
            return self.with_context(state='vice_principal', message_users=[p.id for p in self.request_principal_vice_principals]).common_apply()
        elif self.principal_apply_type == 'department':
            self.write({'request_principal_vice_principals': [(5, 0, 0)],
                        'request_department_teacher_users': [(5, 0, 0)]})
            return self.with_context(state='department').common_apply()
        elif self.principal_apply_type == 'to_end':
            self.write({'request_department_users': [(5, 0, 0)],
                        'request_department_teacher_users': [(5, 0, 0)],
                        'request_principal_vice_principals': [(5, 0, 0)]})
            return self.with_context(state='finish').common_apply()
        else:
            self.write({'request_principal_vice_principals': [(5, 0, 0)]})
            self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.request_department_teacher_users]})
            return self.common_apply()

    @api.multi
    def vice_principal_apply(self):
        if self.vice_principal_apply_type == 'department':
            self.write({'request_vice_department_teacher_users': [(5, 0, 0)],
                        })
            return self.with_context(state='department').common_apply()
        elif self.vice_principal_apply_type == 'teacher':
            self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.request_vice_department_teacher_users]})
            return self.with_context(state='finish_teacher').common_apply()
        elif self.vice_principal_apply_type == 'to_end':
            self.write({
                'request_vice_department_teacher_users': [(5, 0, 0)],
                'request_vice_department_users': [(5, 0, 0)],
            })
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
        if self.department_apply_type == 'teacher':
            self.write({'results': [(5, 0), ] + [(0, 0, {'user': u.id, 'transform': self.id}) for u in self.department_comment_user]})
            self.common_apply()
        elif self.department_apply_type == 'to_end':
            self.write({
                'department_comment_user': [(5, 0, 0)],
            })
            return self.with_context(state='finish').common_apply()

    @api.multi
    def button_teacher_finish(self):
        results = self.results.filtered(lambda result: result.user.id == self.env.uid)
        results.write({
            'finish_date': fields.Datetime.now(),
            'state': 'finished',
            'comment': self.env.context['message'] if 'message' in self.env.context else False,
        })
        if len(self.results.filtered(lambda result: result.state == 'finished')) == len(self.results):
            self.state = 'finish'

    @api.multi
    def button_reject_teacher_finish(self):
        if self.department_user:
            state = 'department'
        elif self.vice_principal_user:
            state = 'vice_principal'
        else:
            state = 'principal'
        self.write({
            'results': [(2, r.id, 0) for r in self.results]
        })
        return self.with_context(state=state).common_reject()

    @api.v7
    def fix_change_principal_problem(self, cr, uid, context=None):
        docs = self.browse(cr, 1, self.search(cr, 1, [(1, '=', 1)], context), context)
        for doc in docs:
            if doc.request_principal_vice_principal:
                self.write(cr, 1, doc.id, {
                    'request_principal_vice_principals': [(6, 0, [doc.request_principal_vice_principal.id])]
                }, context)


class UserResult(models.Model):
    _name = 'ft.document.transform.result'
    _description = 'Doc Transform Result'
    _rec_name = 'user'

    transform = fields.Many2one('ft.document.transform', 'Related Transform', ondelete='cascade')
    user = fields.Many2one('res.users', 'User')
    finish_date = fields.Datetime('Finished Time')
    state = fields.Selection([('processing', u'处理中'), ('finished', u'完成')], 'State', default='processing')
    comment = fields.Char('Comment')







