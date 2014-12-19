__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Cource(models.Model):
    _name = 'school.course'

    name = fields.Char('Name', required=True)


class Class(models.Model):
    _name = 'school.class'

    name = fields.Char('Name', required=True)


class Semester(models.Model):
    _name = 'school.semester'

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
