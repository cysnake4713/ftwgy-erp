# coding=utf-8
import datetime
import pytz

__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class Plan(models.Model):
    _name = 'school.timetable.plan'
    _inherit = ['school.timetable.cell.abstract', 'mail.thread']
    _order = 'start_date,lesson,classroom,subject'

    start_date = fields.Date('Start Date')

    start_datetime = fields.Datetime('Start Datetime', compute='_compute_plan_datetimes')
    end_datetime = fields.Datetime('End Datetime', compute='_compute_plan_datetimes')

    lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Lesson Type')

    color_partner_id = fields.Integer(string="colorize", compute='_color_partner')
    active = fields.Boolean('Is Active')

    _defaults = {
        'active': True,
    }

    @api.one
    @api.depends('teacher.partner_id')
    def _color_partner(self):
        self.color_partner_id = self.teacher.partner_id.id

    @api.multi
    @api.depends('lesson_type', 'lesson', 'start_date')
    def _compute_plan_datetimes(self):
        for plan in self:
            plan.start_datetime = self._get_lesson_time(plan.start_date, plan.lesson, 'start_date', plan.lesson_type, )
            plan.end_datetime = self._get_lesson_time(plan.start_date, plan.lesson, 'end_date', plan.lesson_type, )

    @api.model
    def _get_lesson_time(self, origin_date, lesson, field, type):
        if not (origin_date and lesson):
            return None
        else:
            if type == 'summer' and field == 'start_date':
                target_time = lesson.summer_start_time
            elif type == 'summer' and field == 'end_date':
                target_time = lesson.summer_end_time
            elif type == 'winter' and field == 'start_date':
                target_time = lesson.winter_start_time
            elif type == 'winter' and field == 'end_date':
                target_time = lesson.winter_end_time
            else:
                return None
            return self._utc_timestamp(datetime.datetime.strptime(origin_date, DEFAULT_SERVER_DATE_FORMAT) + datetime.timedelta(hours=target_time))

    @api.model
    def _utc_timestamp(self, timestamp):
        """Returns the given timestamp converted to the client's timezone.
           This method is *not* meant for use as a _defaults initializer,
           because datetime fields are automatically converted upon
           display on client side. For _defaults you :meth:`fields.datetime.now`
           should be used instead.

           :param datetime timestamp: naive datetime value (expressed in UTC)
                                      to be converted to the client timezone
           :rtype: datetime
           :return: timestamp converted to timezone-aware datetime in context
                    timezone
        """
        assert isinstance(timestamp, datetime.datetime), 'Datetime instance expected'
        tz_name = self._context.get('tz') or self.env.user.tz
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            context_timestamp = context_tz.localize(timestamp, is_dst=False)  # UTC = no DST
            return context_timestamp.astimezone(utc)
        return timestamp

    @api.multi
    @api.depends('start_date', 'lesson', 'teacher', 'classroom', 'subject')
    def name_get(self):
        result = []
        for plan in self:
            result.append(
                (plan.id, u'(%s 第%s节)%s %s %s' % (plan.start_date, plan.lesson.name, plan.teacher.name, plan.classroom.name, plan.subject.name)))
        return result


class PlanWizard(models.Model):
    _name = 'school.timetable.plan.switch.wizard'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], 'State')
    origin_plan = fields.Many2one('school.timetable.plan', 'Origin Plan')
    target_plan = fields.Many2one('school.timetable.plan', 'Target Plan')

    result_origin_plan = fields.Many2one('school.timetable.plan', 'Result Origin Plan')
    result_target_plan = fields.Many2one('school.timetable.plan', 'Result Target Plan')

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
        self.state = 'confirmed'

    @api.multi
    def button_reverse_plan(self):
        self.result_origin_plan.unlink()
        self.result_target_plan.unlink()

        self.origin_plan.active = True
        self.target_plan.active = True
        self.state = 'draft'