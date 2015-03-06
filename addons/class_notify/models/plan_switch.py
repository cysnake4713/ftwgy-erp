__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class PlanWizard(models.Model):
    _name = 'school.timetable.plan.switch.wizard'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], 'State', default='draft')
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