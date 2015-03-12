# coding=utf-8
__author__ = 'cysnake4713'

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import datetime


class Subject(models.Model):
    _name = 'school.subject'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    short_name = fields.Char('Short Name')

    _sql_constraints = [('school_subject_unique', 'unique(name)', _('name must be unique !'))]


class ClassRoom(models.Model):
    _name = 'school.classroom'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)

    _sql_constraints = [('school_classroom_unique', 'unique(name)', _('name must be unique !'))]


class Lesson(models.Model):
    _name = 'school.lesson'
    _rec_name = 'name'

    name = fields.Integer('Name', required=True)
    summer_start_time = fields.Float('Summer Start Time', required=True)
    summer_end_time = fields.Float('Summer End Time', required=True)
    winter_start_time = fields.Float('Winter Start Time', required=True)
    winter_end_time = fields.Float('Winter End Time', required=True)


class Semester(models.Model):
    _name = 'school.semester'
    _order = 'end_date desc'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    @api.multi
    @api.depends('name', 'start_date', 'end_date')
    def name_get(self):
        result = []
        for semester in self:
            result.append((semester.id, u'%s (%s - %s)' % (semester.name, semester.start_date, semester.end_date)))
        return result

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_date_period(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise Warning(_('End Date cannot be set before Start Date.'))