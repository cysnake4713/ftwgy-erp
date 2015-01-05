__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class TempDepartment(models.Model):
    _name = 'hr.department'

    name = fields.Char('Name', required=True)


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one('hr.department', 'Department')

