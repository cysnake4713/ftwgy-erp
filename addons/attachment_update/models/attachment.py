__author__ = 'cysnake4713'
# coding=utf-8

import logging

_logger = logging.getLogger(__name__)
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class AttachmentInherit(models.Model):
    _inherit = 'ir.attachment'

    @api.v7
    def get_attachment_file(self, cr, uid, id, context):

        attachment = self.browse(cr, uid, id, context)

        full_path = self._full_path(cr, uid, attachment.store_fname)
        r = open(full_path, 'rb')
        return attachment.name, r


        # def a_data_set(self, cr, uid, id, name, value, arg, context=None):
        # # We dont handle setting data to null
        # if not value:
        #         return True
        #     if context is None:
        #         context = {}
        #     location = self._storage(cr, uid, context)
        #     file_size = len(value.decode('base64')) if isinstance(value, str) else 0
        #     attach = self.browse(cr, uid, id, context=context)
        #     fname_to_delete = attach.store_fname
        #     if location != 'db':
        #         fname, file_size = self._file_write(cr, uid, value)
        #         # SUPERUSER_ID as probably don't have write access, trigger during create
        #         super(AttachmentInherit, self).write(cr, SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size, 'db_datas': False},
        #                                              context=context)
        #     else:
        #         super(AttachmentInherit, self).write(cr, SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size, 'store_fname': False},
        #                                              context=context)
        #
        #     # After de-referencing the file in the database, check whether we need
        #     # to garbage-collect it on the filesystem
        #     if fname_to_delete:
        #         self._file_delete(cr, uid, fname_to_delete)
        #     return True
        #
        # def _data_set(self, cr, uid, id, name, value, arg, context=None):
        #     # We dont handle setting data to null
        #     if not value:
        #         return True
        #     if context is None:
        #         context = {}
        #     location = self._storage(cr, uid, context)
        #     file_size = len(value.decode('base64'))
        #     attach = self.browse(cr, uid, id, context=context)
        #     fname_to_delete = attach.store_fname
        #     if location != 'db':
        #         fname = self._file_write(cr, uid, value)
        #         # SUPERUSER_ID as probably don't have write access, trigger during create
        #         super(AttachmentInherit, self).write(cr, SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size, 'db_datas': False}, context=context)
        #     else:
        #         super(AttachmentInherit, self).write(cr, SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size, 'store_fname': False}, context=context)
        #
        #     # After de-referencing the file in the database, check whether we need
        #     # to garbage-collect it on the filesystem
        #     if fname_to_delete:
        #         self._file_delete(cr, uid, fname_to_delete)
        #     return True
        #
        # def _file_read(self, cr, uid, fname, bin_size=False):
        #     full_path = self._full_path(cr, uid, fname)
        #     r = ''
        #     try:
        #         if bin_size:
        #             r = os.path.getsize(full_path)
        #         else:
        #             r = open(full_path, 'rb')
        #     except IOError:
        #         _logger.exception("_read_file reading %s", full_path)
        #     return r
        #
        #
        # def _data_get(self, cr, uid, ids, name, arg, context=None):
        #     if context is None:
        #         context = {}
        #     result = {}
        #     bin_size = context.get('bin_size')
        #     for attach in self.browse(cr, uid, ids, context=context):
        #         if attach.store_fname:
        #             result[attach.id] = self._file_read(cr, uid, attach.store_fname, bin_size)
        #         else:
        #             result[attach.id] = attach.db_datas
        #     return result
        #
        # _columns = {
        #     'datas': fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
        # }
