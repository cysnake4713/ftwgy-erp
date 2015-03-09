__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class WorkflowAbstract(models.AbstractModel):
    _name = 'odoosoft.workflow.abstract'
    _inherit = 'mail.thread'

    _state_field_map = {}

    @api.multi
    def _update_state(self, vals, is_apply=False):
        '''
        'state'
        'body': vals['message'],
        'subject': vals.get('subject', None),
        'type': vals.get('type', 'notification'),
        'content_subtype': vals.get('content_subtype', 'html'),
        'user_ids': vals.get('message_users', None),
        'mail_create_nosubscribe': not vals.get('auto_subscribe', False),
        '''

        def _get_signature_values(need_write_state):
            result = {}
            if need_write_state in self._state_field_map:
                if isinstance(self._state_field_map[need_write_state], bool):
                    if self._state_field_map[need_write_state]:
                        result.update({
                            need_write_state + '_user': self.env.uid if is_apply else None,
                            need_write_state + '_datetime': fields.Datetime.now() if is_apply else None,
                        })
                else:
                    state_map = self._state_field_map[need_write_state]
                    for user in state_map.get('user', []):
                        result.update({
                            user: self.env.uid if is_apply else None,
                        })
                    for time in state_map.get('time', []):
                        result.update({
                            time: fields.Datetime.now() if is_apply else None,
                        })
            return result

        # state
        if 'state' not in vals:
            raise exceptions.Warning('Must have state defined in value during apply_state!')

        # mail.message
        # if defined message
        if 'message' in vals:
            user_ids = vals.get('message_users', None)
            if user_ids and isinstance(user_ids, list) and len(user_ids) > 0 and isinstance(user_ids[0], list) and isinstance(user_ids[0][2], list):
                user_ids = user_ids[0][2]
            mail_value = {
                'body': vals['message'],
                'subject': vals.get('subject', None),
                'type': vals.get('type', 'notification'),
                'content_subtype': vals.get('content_subtype', 'html'),
                'user_ids': user_ids,
            }
            self.with_context({
                # 'mail_post_autofollow': vals.get('mail_post_autofollow', False),
                'mail_create_nosubscribe': not vals.get('auto_subscribe', False),
            }).message_post(**mail_value)

        # write
        for obj in self:
            # if is apply state, write signature
            signature_values = _get_signature_values(obj.state) if is_apply else _get_signature_values(vals['state'])
            signature_values.update({'state': vals['state']})
            obj.write(signature_values)
        return True

    @api.multi
    def common_apply(self):
        values = self.env.context.copy()
        return self._update_state(values, True)

    @api.multi
    def common_reject(self):
        values = self.env.context.copy()
        return self._update_state(values, False)

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
            user_ids += kwargs['user_ids'] if isinstance(kwargs['user_ids'], list) else [kwargs['user_ids']]
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

        return super(WorkflowAbstract, self).message_post(cr, uid, thread_id, body=body, subject=subject, type=type,
                                                          subtype=subtype, parent_id=parent_id, attachments=attachments, context=context,
                                                          content_subtype=content_subtype, partner_ids=partner_ids, **kwargs)

