__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class CurriculumCell(models.Model):
    _name = 'school.timetable.cell'

    teacher = fields.Many2one('res.users')
    # 科目
    subject = fields.Many2one('school.subject')
    # 班级
    classroom = fields.Many2one('school.classroom')
    # 周几
    week = fields.Selection([("Monday", "星期一"), ("Tuesday", "星期二"),
                             ("Wednesday", "星期三"), ("Thursday", "星期四"),
                             ("Friday", "星期五"), ("Saturday", "星期六"), ("Sunday", "星期日")], 'Week')
    # 第几节课
    lesson = fields.Integer('Lesson')

    timetable_id = fields.Many2one('school.timetable', 'Timetable', ondelete='cascade')


class Curriculum(models.Model):
    _name = 'school.timetable'
    _rec_name = 'semester_id'

    semester_id = fields.Many2one('school.semester', required=True)
    cell_ids = fields.One2many('school.timetable.cell', 'timetable_id', 'Cells')
