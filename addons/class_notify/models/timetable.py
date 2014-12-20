__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class CellAbstract(models.AbstractModel):
    _name = 'school.timetable.cell.abstract'

    teacher = fields.Many2one('res.users')
    # 科目
    subject = fields.Many2one('school.subject')
    # 班级
    classroom = fields.Many2one('school.classroom')
    # 周几
    week = fields.Selection([("Monday", u"星期一"), ("Tuesday", u"星期二"),
                             ("Wednesday", u"星期三"), ("Thursday", u"星期四"),
                             ("Friday", u"星期五"), ("Saturday", u"星期六"), ("Sunday", u"星期日")], 'Week')
    # 第几节课
    lesson = fields.Many2one('school.lesson', 'Lesson')


class CurriculumCell(models.Model):
    _name = 'school.timetable.cell'
    _inherit = 'school.timetable.cell.abstract'

    timetable_id = fields.Many2one('school.timetable', 'Timetable', ondelete='cascade')


class Curriculum(models.Model):
    _name = 'school.timetable'
    _rec_name = 'semester_id'

    semester_id = fields.Many2one('school.semester', required=True)
    cell_ids = fields.One2many('school.timetable.cell', 'timetable_id', 'Cells')

    # lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Lesson Type')
