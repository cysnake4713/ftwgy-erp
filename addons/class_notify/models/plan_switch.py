# coding=utf-8
__author__ = 'cysnake4713'

from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _

from datetime import date, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class PlanWizard(models.Model):
    _name = 'school.timetable.plan.switch.wizard'
    _inherit = 'odoosoft.workflow.abstract'
    _rec_name = 'origin_plan'
    _order = 'id desc'
    _description = 'School Timetable Wizard'

    _state_field_map = {
        'draft': True,
        'target_teacher': True,
        'center_confirm': True,
    }

    state = fields.Selection(
        [('draft', 'Draft'), ('target_teacher', 'Target Teacher Confirm'), ('center_confirm', 'Center Confirm'), ('confirmed', 'Confirmed'),
         ('cancel', 'Cancel')], 'State', track_visibility='onchange', default='draft')

    origin_plan = fields.Many2one('school.timetable.plan', 'Need To Switch')
    origin_plan_teacher = fields.Many2one('res.users', 'Origin Teacher', compute='_compute_plan_info')
    origin_plan_classroom = fields.Many2one('school.classroom', 'Origin Plan Classroom', compute='_compute_plan_info')
    # origin_plan_date = fields.Date('Origin Plan Date',compute='_compute_origin_plan_info')
    # origin_plan_lesson = fields.Many2one('school.lesson', 'Origin Plan Lesson', compute='_compute_origin_plan_info')

    target_plan = fields.Many2one('school.timetable.plan', 'Switch To')
    target_plan_teacher = fields.Many2one('res.users', 'Target Teacher', compute='_compute_plan_info')

    result_origin_plan = fields.Many2one('school.timetable.plan', 'Result Origin Plan')
    result_target_plan = fields.Many2one('school.timetable.plan', 'Result Target Plan')

    target_teacher_user = fields.Many2one('res.users', 'Target Teacher User')
    target_teacher_datetime = fields.Datetime('Target Teacher Datetime')

    head_teacher = fields.Many2many('res.users', 'class_plan_wizard_head_user_rel', 'plan_id', 'user_id', 'Head Teacher')

    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Datetime')

    request_center_user = fields.Many2one('res.users', 'Request Center Confirm User')
    center_confirm_user = fields.Many2one('res.users', 'Center Confirm User')
    center_confirm_datetime = fields.Datetime('Center Confirm Datetime')

    @api.multi
    def name_get(self):
        result = []
        for plan in self:
            result.append((plan.id, u'换课申请记录'))
        return result

    @api.one
    @api.depends('origin_plan', 'target_plan')
    def _compute_plan_info(self):
        self.origin_plan_classroom = self.origin_plan.classroom
        self.origin_plan_teacher = self.origin_plan.teacher
        self.target_plan_teacher = self.target_plan.teacher

    @api.constrains('origin_plan', 'target_plan')
    def _constrains_origin_target_plan(self):

        result = self.env['school.timetable.plan'].search(
            [('teacher', '=', self.target_plan.teacher.id), ('start_date', '=', self.origin_plan.start_date),
             ('lesson', '=', self.origin_plan.lesson.id)])
        if result:
            raise exceptions.Warning(_("target plan teacher's plan is conflict to the origin plan date and lesson!"))

    @api.multi
    def switch_plan_confirm(self):
        if not (self.origin_plan or self.target_plan):
            raise exceptions.Warning(_('Must have both Origin Plan and Target Plan!'))
        sudo_user = self.sudo()

        result_origin_plan = sudo_user.origin_plan.copy()
        result_target_plan = sudo_user.target_plan.copy()

        result_origin_plan.teacher = self.target_plan.teacher
        result_origin_plan.subject = self.target_plan.subject

        result_target_plan.teacher = self.origin_plan.teacher
        result_target_plan.subject = self.origin_plan.subject

        sudo_user.result_target_plan = result_target_plan
        sudo_user.result_origin_plan = result_origin_plan

        sudo_user.origin_plan.active = False
        sudo_user.target_plan.active = False

        origin_timetable = sudo_user.env['school.timetable'].search([('plan_ids', '=', self.origin_plan.id)])
        origin_timetable.write({'plan_ids': [(4, self.result_origin_plan.id)]})
        target_timetable = sudo_user.env['school.timetable'].search([('plan_ids', '=', self.target_plan.id)])
        target_timetable.write({'plan_ids': [(4, self.result_target_plan.id)]})

        self.send_notify_mail(self.origin_plan, self.result_target_plan)
        self.send_notify_mail(self.target_plan, self.result_origin_plan)
        self.send_notify_mail_to_head(self.target_plan, self.result_origin_plan, self.origin_plan, self.result_target_plan, self.head_teacher)
        self.state = 'confirmed'

    @api.multi
    def send_notify_mail(self, origin_plan, target_plan):
        if origin_plan and target_plan:
            text = u'您的课程:%s 调换到了:%s,<br/>请注意上课时间' % (origin_plan.name_get()[0][1], target_plan.name_get()[0][1])
            self.with_context({
                'message_users': [origin_plan.teacher.id],
                'message': text,
                'wechat_code': ['class_notify.plan_swtich'],
                'wechat_template': 'class_notify.message_template_plan_switch',
            }).common_apply()

    @api.multi
    def send_notify_mail_to_head(self, origin_plan, target_plan, s_origin_plan, s_target_plan, teachers):
        if origin_plan and target_plan:
            text = u'课程:%s 调换到了:%s,<br/>' \
                   u'课程:%s 调换到了:%s,<br/>' \
                   u'请注意本班课程变更' % (
                       origin_plan.name_get()[0][1], target_plan.name_get()[0][1],
                       s_origin_plan.name_get()[0][1], s_target_plan.name_get()[0][1],)
            self.with_context({
                'message_users': [t.id for t in teachers],
                'message': text,
                'wechat_code': ['class_notify.plan_swtich'],
                'wechat_template': 'class_notify.message_template_plan_switch',
            }).common_apply()


    @api.model
    def cron_send_notify_mail(self):
        tomorrow = (date.today() + timedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
        need_notify_plan = self.search([('state', '=', 'confirmed'), ('result_origin_plan.start_date', '=', tomorrow)])
        for plan in need_notify_plan:
            plan.send_notify_mail(plan.target_plan, plan.result_origin_plan)

        need_notify_plan = self.search([('state', '=', 'confirmed'), ('result_target_plan.start_date', '=', tomorrow)])
        for plan in need_notify_plan:
            plan.send_notify_mail(plan.origin_plan, plan.result_target_plan)

    @api.multi
    def button_reverse_plan(self):
        self.send_notify_mail(self.result_target_plan, self.origin_plan)
        self.send_notify_mail(self.result_origin_plan, self.target_plan)

        self.result_origin_plan.unlink()
        self.result_target_plan.unlink()

        self.origin_plan.active = True
        self.target_plan.active = True
        self.state = 'draft'