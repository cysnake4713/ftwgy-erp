__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Plan(models.Model):
    _name = 'school.timetable.plan'
    _inherit = 'school.timetable.cell.abstract'

    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    lesson_type = fields.Selection([('summer', u'夏时'), ('winter', u'冬时')], 'Lesson Type')

    color_partner_id = fields.Integer(string="colorize", compute='_color_partner')

    @api.one
    @api.depends('teacher.partner_id')
    def _color_partner(self):
        self.color_partner_id = self.teacher.partner_id.id