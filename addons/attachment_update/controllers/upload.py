__author__ = 'cysnake4713'

import simplejson
from openerp.addons.web.controllers.main import Binary, content_disposition, serialize_exception
from openerp import http
from openerp.http import request
from openerp.tools.translate import _


class BinaryExtend(Binary):
    def attachment_saveas(self, model, field, id=None, filename_field=None, **kw):
        Model = request.session.model(model)
        filename, outfile = Model.get_attachment_file(int(id), request.context)
        if not outfile:
            return request.not_found()
        else:
            return request.make_response(outfile,
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition', content_disposition(filename))])

    @http.route('/web/binary/saveas', type='http', auth="public")
    @serialize_exception
    def saveas(self, model, field, id=None, filename_field=None, **kw):
        if model == 'ir.attachment':
            return self.attachment_saveas(model, field, id, filename_field, **kw)
        else:
            return super(BinaryExtend, self).saveas(model, field, id, filename_field, **kw)

    def attachment_saveas_ajax(self, data, token):
        jdata = simplejson.loads(data)
        id = jdata.get('id', None)
        attachment_obj = request.session.model('ir.attachment')
        if id:
            filename, outfile = attachment_obj.get_attachment_file(int(id), request.context)
            return request.make_response(outfile,
                                         headers=[('Content-Type', 'application/octet-stream'),
                                                  ('Content-Disposition', content_disposition(filename))],
                                         cookies={'fileToken': token})
        else:
            raise ValueError(_("No attachment found for id '%s'") % id)


    @http.route('/web/binary/saveas_ajax', type='http', auth="public")
    @serialize_exception
    def saveas_ajax(self, data, token):
        jdata = simplejson.loads(data)
        if jdata['model'] == 'ir.attachment':
            return self.attachment_saveas_ajax(data, token)
        else:
            return super(BinaryExtend, self).saveas_ajax(data, token)