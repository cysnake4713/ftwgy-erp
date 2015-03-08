__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class WorkflowAbstract(models.AbstractModel):
    _name = 'odoosoft.workflow.abstract'
    _state_field_map = {}

    @api.multi
    def _update_state(self, vals, is_apply=False):

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

        if 'state' not in vals:
            raise exceptions.Warning('Must have state defined in value during apply_state!')
        for obj in self:
            # if is apply state, write signature
            signature_values = _get_signature_values(obj.state) if is_apply else _get_signature_values(vals['state'])
            signature_values.update({'state': vals['state']})
            obj.write(signature_values)

        # sms_msg = vals.get('sms', '')
        # subject = u'项目负责人和主管总师变更申请'
        # context['mail_create_nosubscribe'] = True
        # if vals['target'] == 'suozhang':
        # suzhang_ids = self.pool['res.users'].get_department_suzhang_ids(cr, uid, [uid], context=context)
        # # zhurengong_ids = self.pool['res.users'].get_department_zhurengong_ids(cr, uid, [uid], context=context)
        # self.message_post(cr, uid, ids, body=sms_msg, subject=subject, subtype='mail.mt_comment', type='comment', context=context,
        # user_ids=suzhang_ids, is_send_sms=True)
        # if vals['target'] == 'group':
        # group_id = vals['group_ids']
        # self.message_post(cr, uid, ids, body=sms_msg, subject=subject, subtype='mail.mt_comment', type='comment', context=context,
        # group_xml_ids=group_id, is_send_sms=True)
        # if vals['target'] == 'user':
        # user_ids = vals['user_ids']
        # self.message_post(cr, uid, ids, body=sms_msg, subject=subject, subtype='mail.mt_comment', type='comment', context=context,
        # user_ids=user_ids, is_send_sms=True)
        return True

    @api.multi
    def common_apply(self, values=None):
        return self._update_state(values, True)

    @api.multi
    def common_reject(self, values=None):
        return self._update_state(values, False)
