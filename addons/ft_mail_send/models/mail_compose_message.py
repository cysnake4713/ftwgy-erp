__author__ = 'cysnak4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _


class MailComposeMessageInherit(models.TransientModel):
    _inherit = 'mail.compose.message'

    departments = fields.Many2many('hr.department', 'compose_message_department_rel', 'compose_id', 'user_id', 'Need Send Departments')

    @api.multi
    def send_mail_multi(self):
        if not (self.res_users or self.departments):
            raise exceptions.Warning(_('At least select one department or user!'))
        department_partner_ids = []
        for department in self.departments:
            department_partner_ids += [u.partner_id.id for u in department.users if u.partner_id]
        user_partner_ids = [u.partner_id.id for u in self.res_users]
        res_partners = list(set(department_partner_ids + user_partner_ids))
        self.write({
            'partner_ids': [(6, 0, res_partners)]
        })
        self.send_mail()
