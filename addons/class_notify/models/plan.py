# coding=utf-8
import datetime

__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Plan(models.Model):
    _name = 'school.timetable.plan'
    _inherit = 'school.timetable.cell.abstract'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    start_datetime = fields.Datetime('Start Datetime', compute='_compute_plan_datetimes')
    end_datetime = fields.Datetime('End Datetime', compute='_compute_plan_datetimes')

    lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Lesson Type')

    color_partner_id = fields.Integer(string="colorize", compute='_color_partner')

    @api.one
    @api.depends('teacher.partner_id')
    def _color_partner(self):
        self.color_partner_id = self.teacher.partner_id.id

    @api.multi
    @api.depends('lesson_type', 'lesson', 'start_date', 'end_date')
    def _compute_plan_datetimes(self):
        for plan in self:
            plan.start_datetime = self._get_lesson_time(plan.start_date, plan.lesson, 'start_date', plan.lesson_type, )
            plan.end_datetime = self._get_lesson_time(plan.end_date, plan.lesson, 'end_date', plan.lesson_type, )
            # plan.start_datetime = None

    @api.model
    def _get_lesson_time(self, origin_date, lesson, field, type):
        if not (origin_date and lesson):
            return None
        else:
            if type == 'summer' and field == 'start_date':
                target_time = lesson.summer_start_time.split(' ')[1]
            elif type == 'summer' and field == 'end_date':
                target_time = lesson.summer_end_time.split(' ')[1]
            elif type == 'winter' and field == 'start_date':
                target_time = lesson.winter_start_time.split(' ')[1]
            elif type == 'winter' and field == 'end_date':
                target_time = lesson.winter_end_time.split(' ')[1]
            else:
                return None
            return datetime.datetime.strptime(origin_date + ' ' + target_time, DEFAULT_SERVER_DATETIME_FORMAT)