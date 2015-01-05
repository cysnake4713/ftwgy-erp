__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectInherit(models.Model):
    _inherit = 'project.project'

    department_id = fields.Many2one('hr.department', 'Department')


class TaskInherit(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', 'Department')
