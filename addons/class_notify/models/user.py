__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ResUserInheirt(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_group(self):
        result = super(ResUserInheirt, self)._get_group()
        dataobj = self.pool.get('ir.model.data')
        try:
            result.append(self.env.ref('class_notify.group_class_user').id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result

    _defaults = {
        'groups_id': _get_group,
    }
