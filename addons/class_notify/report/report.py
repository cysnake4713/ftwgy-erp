# coding=utf-8
import collections
from openerp.report import report_sxw

__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Timetable(report_sxw.rml_parse):
    def set_context(self, objects, data, ids, report_type=None):
        self.weeks = collections.OrderedDict([
            ("Monday", u"星期一"), ("Tuesday", u"星期二"),
            ("Wednesday", u"星期三"), ("Thursday", u"星期四"),
            ("Friday", u"星期五"),
            # ("Saturday", u"星期六"), ("Sunday", u"星期日")
        ])
        self.ids = ids

        classroom_obj = self.pool['school.classroom']
        self.classrooms = classroom_obj.browse(self.cr, self.uid, classroom_obj.search(self.cr, self.uid, []), context=self.localcontext)

        lesson_obj = self.pool['school.lesson']
        self.lessons = lesson_obj.browse(self.cr, self.uid, lesson_obj.search(self.cr, self.uid, [], order='name'), context=self.localcontext)

        cell_obj = self.pool['school.timetable.cell']
        cells = cell_obj.search_read(self.cr, self.uid, [('timetable_id', 'in', self.ids)], ['classroom', 'week', 'lesson', 'subject', 'teacher'],
                                     context=self.localcontext)
        lesson_map = {}
        for cell in cells:
            lesson_map[(cell['classroom'][0], cell['week'], cell['lesson'][0])] = (
                cell['subject'][1] if 'subject' in cell else '',
                cell['teacher'][1] if 'teacher' in cell else '',)

        self.localcontext.update({
            'classrooms': self.classrooms,
            'weeks': self.weeks,
            'lessons': self.lessons,
            'lesson_map': lesson_map,
            'get_lesson_detail': self._get_lesson_detail,

        })
        return super(Timetable, self).set_context(objects, data, ids, report_type=report_type)

    def _get_lesson_detail(self, week, lesson, classroom):
        lesson_map = self.localcontext['lesson_map']
        if (classroom.id, week, lesson.id) in lesson_map:
            detail = lesson_map[(classroom.id, week, lesson.id)]
            return '%s<br/>%s' % (detail[0], detail[1])
        else:
            return None


class ReportTimetable(models.AbstractModel):
    _name = 'report.class_notify.report_timetable'
    _inherit = 'report.abstract_report'
    _template = 'class_notify.report_timetable'
    _wrapped_report_class = Timetable
