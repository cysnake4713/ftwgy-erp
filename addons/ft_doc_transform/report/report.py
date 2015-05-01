# coding=utf-8
from openerp.report import report_sxw

__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class DocTransform(report_sxw.rml_parse):
    def set_context(self, objects, data, ids, report_type=None):

        self.localcontext.update({
            'object': self.pool['ft.document.transform'].browse(self.cr, self.uid, ids[0], context=self.localcontext),

        })
        return super(DocTransform, self).set_context(objects, data, ids, report_type=report_type)

    def _get_lesson_detail(self, week, lesson, classroom):
        lesson_map = self.localcontext['lesson_map']
        if (classroom.id, week, lesson.id) in lesson_map:
            detail = lesson_map[(classroom.id, week, lesson.id)]
            return '%s<br/>%s' % (detail[0], detail[1])
        else:
            return None


class ReportTimetable(models.AbstractModel):
    _name = 'report.ft_doc_transform.report_doc_transform'
    _inherit = 'report.abstract_report'
    _template = 'ft_doc_transform.report_doc_transform'
    _wrapped_report_class = DocTransform
