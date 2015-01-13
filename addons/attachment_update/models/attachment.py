__author__ = 'cysnake4713'
# coding=utf-8

import hashlib
import os
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

    @api.v7
    def set_attachment_file(self, cr, uid, name, ufile, datas_fname, res_model, res_id, context):
        if context is None:
            context = {}
        file_size = 0
        sha1 = hashlib.sha1()
        while True:
            # read 16MB
            block = ufile.read(16 * 1024 * 1024)
            if block:
                sha1.update(block)
            else:
                break
        fname = sha1.hexdigest()
        fname = fname[:3] + '/' + fname
        full_path = self._full_path(cr, uid, fname)
        try:
            ufile.seek(0, 0)
            dirname = os.path.dirname(full_path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            ufile.save(full_path)
            file_size = os.path.getsize(full_path)
        except IOError:
            _logger.error("_file_write writing %s", full_path)

        # create db record
        return self.create(cr, uid, {
            'name': name,
            'store_fname': fname,
            'file_size': file_size,
            'datas_fname': datas_fname,
            'res_id': res_id,
            'res_model': res_model,
        }, context=context)