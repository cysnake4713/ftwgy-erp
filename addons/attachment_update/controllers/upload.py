__author__ = 'cysnake4713'

from openerp.addons.web.controllers.main import Binary, content_disposition, serialize_exception
from openerp import http
from openerp.http import request


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
