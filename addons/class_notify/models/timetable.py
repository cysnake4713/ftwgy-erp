# coding=utf-8
from openerp.osv import osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from dateutil import rrule, parser


class CellAbstract(models.AbstractModel):
    _name = 'school.timetable.cell.abstract'

    teacher = fields.Many2one('res.users')
    # 科目
    subject = fields.Many2one('school.subject', required=True)
    # 班级
    classroom = fields.Many2one('school.classroom', required=True)
    # 第几节课
    lesson = fields.Many2one('school.lesson', 'Lesson', required=True)


class CurriculumCell(models.Model):
    _name = 'school.timetable.cell'
    _inherit = 'school.timetable.cell.abstract'

    timetable_id = fields.Many2one('school.timetable', 'Timetable', ondelete='cascade')
    # 周几
    week = fields.Selection([("Monday", u"星期一"), ("Tuesday", u"星期二"),
                             ("Wednesday", u"星期三"), ("Thursday", u"星期四"),
                             ("Friday", u"星期五"), ("Saturday", u"星期六"), ("Sunday", u"星期日")], 'Week')


class Curriculum(models.Model):
    _name = 'school.timetable'
    _rec_name = 'semester_id'

    semester_id = fields.Many2one('school.semester', required=True)
    cell_ids = fields.One2many('school.timetable.cell', 'timetable_id', 'Cells')

    initial_lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Initial Lesson Type', required=True)
    plan_ids = fields.Many2many('school.timetable.plan', 'timetable_plan_rel', 'timetable_id', 'plan_id', string='Plans')


    @api.one
    def button_generate_plans(self):
        week_map = {"Monday": 0, "Tuesday": 1,
                    "Wednesday": 2, "Thursday": 3,
                    "Friday": 4, "Saturday": 5, "Sunday": 6}
        if self.plan_ids:
            raise osv.except_osv(_('Warning'), _('Current timetable already have plans!'))

        week_dict = self._get_date_week_dict(self.semester_id.start_date, self.semester_id.end_date)
        for cell in self.cell_ids:
            value = self.pool['school.timetable.cell'].copy_data(self.env.cr, self.env.uid, cell.id, context={})
            value['lesson_type'] = self.initial_lesson_type
            del (value['week'])
            del (value['timetable_id'])
            for target_date in week_dict[week_map[cell.week]]:
                value['start_date'] = target_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                self.write({'plan_ids': [(0, 0, value)]})
        return True

    @staticmethod
    def _get_date_week_dict(start_date, end_date):
        dates = list(rrule.rrule(rrule.DAILY, dtstart=parser.parse(start_date), until=parser.parse(end_date)))
        result = {}
        for date in dates:
            week = date.weekday()
            if week in result:
                result[week].append(date)
            else:
                result[week] = [date, ]
        return result

    @api.multi
    def button_clear_plans(self):
        for timetable in self:
            timetable.plan_ids.unlink()
        return True

    @api.multi
    def button_clear_cells(self):
        for timetable in self:
            if timetable.plan_ids:
                raise exceptions.Warning(_('Timetable have plans, please delete plans before delete the timetable.'))
            timetable.cell_ids.unlink()
        return True


class TypeChangeWizard(models.TransientModel):
    _name = 'school.timetable.wizard'

    lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Initial Lesson Type', required=True)
    start_date = fields.Date('Start Date', required=True)


    @api.one
    def button_save(self):
        timetable = self.env['school.timetable'].browse(self.env.context['active_id'])
        timetable.initial_lesson_type = self.lesson_type
        plan_ids = timetable.plan_ids.filtered(lambda record: record.start_date >= self.start_date)
        plan_ids.write({'lesson_type': self.lesson_type})
        return True