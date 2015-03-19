__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class PlanWizard(models.Model):
    _name = 'school.timetable.plan.switch.wizard'
    _inherit = 'odoosoft.workflow.abstract'
    _rec_name = 'origin_plan'
    _description = 'School Timetable Wizard'

    state = fields.Selection(
        [('draft', 'Draft'), ('target_teacher', 'Target Teacher Confirm'), ('center_confirm', 'Center Confirm'), ('confirmed', 'Confirmed')], 'State',
        default='draft')

    origin_plan = fields.Many2one('school.timetable.plan', 'Need To Switch')
    origin_plan_classroom = fields.Many2one('school.classroom', 'Origin Plan Classroom', compute='_compute_origin_plan_info')
    # origin_plan_date = fields.Date('Origin Plan Date',compute='_compute_origin_plan_info')
    # origin_plan_lesson = fields.Many2one('school.lesson', 'Origin Plan Lesson', compute='_compute_origin_plan_info')

    target_plan = fields.Many2one('school.timetable.plan', 'Switch To')

    result_origin_plan = fields.Many2one('school.timetable.plan', 'Result Origin Plan')
    result_target_plan = fields.Many2one('school.timetable.plan', 'Result Target Plan')

    @api.one
    @api.depends('origin_plan')
    def _compute_origin_plan_info(self):
        self.origin_plan_classroom = self.origin_plan.classroom
        # self.origin_plan_date = self.origin_plan.start_date
        # self.origin_plan_lesson = self.origin_plan.lesson

    @api.constrains('origin_plan', 'target_plan')
    def _constrains_origin_target_plan(self):

        result = self.env['school.timetable.plan'].search(
            [('teacher', '=', self.target_plan.teacher.id), ('start_date', '=', self.origin_plan.start_date),
             ('lesson', '=', self.origin_plan.lesson.id)])
        if result:
            raise exceptions.Warning(_("target plan teacher's plan is conflict to the origin plan date and lesson!"))

    @api.multi
    def button_switch_plan(self):
        if not (self.origin_plan or self.target_plan):
            raise exceptions.Warning(_('Must have both Origin Plan and Target Plan!'))

        result_origin_plan = self.origin_plan.copy()
        result_target_plan = self.target_plan.copy()

        result_origin_plan.teacher = self.target_plan.teacher
        result_origin_plan.subject = self.target_plan.subject

        result_target_plan.teacher = self.origin_plan.teacher
        result_target_plan.subject = self.origin_plan.subject

        self.result_target_plan = result_target_plan
        self.result_origin_plan = result_origin_plan

        self.origin_plan.active = False
        self.target_plan.active = False

        origin_timetable = self.env['school.timetable'].search([('plan_ids', '=', self.origin_plan.id)])
        origin_timetable.write({'plan_ids': [(4, self.result_origin_plan.id)]})
        target_timetable = self.env['school.timetable'].search([('plan_ids', '=', self.target_plan.id)])
        target_timetable.write({'plan_ids': [(4, self.result_target_plan.id)]})

        self.send_notify_mail(self.origin_plan, self.result_target_plan)
        self.send_notify_mail(self.target_plan, self.result_origin_plan)
        self.state = 'confirmed'

    @api.multi
    def send_notify_mail(self, origin_plan, target_plan):
        if origin_plan and target_plan:
            text = u'您的课程:%s 调换到了:%s,<br/>请注意上课时间' % (origin_plan.name_get()[0][1], target_plan.name_get()[0][1])
            self.with_context({
                'message_users': origin_plan.teacher.id,
                'message': text,
            }).common_apply()


    @api.multi
    def button_reverse_plan(self):
        self.send_notify_mail(self.result_target_plan, self.origin_plan)
        self.send_notify_mail(self.result_origin_plan, self.target_plan)

        self.result_origin_plan.unlink()
        self.result_target_plan.unlink()

        self.origin_plan.active = True
        self.target_plan.active = True
        self.state = 'draft'