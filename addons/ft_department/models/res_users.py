__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class TempDepartment(models.Model):
    _name = 'hr.department'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    users = fields.Many2many('res.users', 'hr_department_users_rel', 'department_id', 'user_id', 'Users')


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2many('hr.department', 'hr_department_users_rel', 'user_id', 'department_id', 'Department')