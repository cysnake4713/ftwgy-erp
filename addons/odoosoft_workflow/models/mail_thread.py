__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class mail_thread(models.AbstractModel):
    _inherit = 'mail.thread'


    @api.cr_uid_ids_context
    def message_post(self, cr, uid, thread_id, body='', subject=None, type='notification',
                     subtype=None, parent_id=False, attachments=None, context=None,
                     content_subtype='html', **kwargs):

        user_ids = []
        """
        # if have group to process
        group_xml_ids = kwargs.pop('group_xml_ids', '')
        if group_xml_ids:
            user_ids = []
            for group_xml_id in group_xml_ids.split(','):
                (module, xml_id) = group_xml_id.split('.')
                group = self.pool.get('ir.model.data').get_object(cr, 1, module, xml_id, context=context)
                if group:
                    user_ids += [user.id for user in group.users]
        """
        # if have user_ids to process
        if 'user_ids' in kwargs and kwargs['user_ids']:
            user_ids += kwargs['user_ids'] if isinstance(kwargs['user_ids'], []) else [kwargs['user_ids']]
        """
        # if have config group
        config_group_id = kwargs.pop('config_group_id', '')
        if config_group_id:
            model_pool = self.pool.get('ir.model.data')
            model_ids = model_pool.search(cr, 1, [('model', '=', 'project.config.sms'), ('name', '=', config_group_id)],
                                          context=context)
            models = model_pool.browse(cr, 1, model_ids, context=context)
            if models:
                groups_pool = self.pool.get("project.config.sms")
                group = groups_pool.browse(cr, 1, models[0].res_id, context=context)
                user_ids += [user.id for user in group.users]
        """
        partner_ids = [user.partner_id.id for user in self.pool.get('res.users').browse(cr, uid, user_ids, context=context)]
        if 'partner_ids' in kwargs:
            partner_ids += kwargs.pop('partner_ids', [])

        return super(self, mail_thread).message_post(cr, uid, thread_id, body=body, subject=subject, type=type,
                                                     subtype=subtype, parent_id=parent_id, attachments=attachments, context=context,
                                                     content_subtype=content_subtype, partner_ids=partner_ids, **kwargs)

