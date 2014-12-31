# coding=utf-8
import base64
import StringIO
import re
import itertools

__author__ = 'cysnake4713'
import csv
from openerp import tools
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _, _logger


class TimetableImport(models.TransientModel):
    _name = 'school.timetable.import'

    data = fields.Binary('Data')
    message = fields.Html('Error Message')
    timetable_id = fields.Integer('Timetable Id')
    state = fields.Selection([('draft', 'Draft'), ('finish', 'Finish')], 'State')

    _defaults = {
        'state': 'draft',
    }

    @staticmethod
    def _get_head(datas):
        week_map = dict([(u"星期一", "Monday"), ( u"星期二", "Tuesday"),
                         ( u"星期三", "Wednesday"), ( u"星期四", "Thursday"),
                         ( u"星期五", "Friday"), ( u"星期六", "Saturday"), ( u"星期日", "Sunday")])
        head_map = {}
        head_week = datas.next()
        head_lesson = datas.next()
        if len(head_week) != len(head_lesson):
            raise (_('The head is not equal'))
        for i in range(1, len(head_week)):
            head_map[i] = (week_map[head_week[i]], head_lesson[i])
        return head_map

    def _convert_import_data(self, import_datas, timetable_id):
        import_fields = ['week', 'lesson', 'classroom', 'subject', 'teacher', 'timetable_id/.id']
        head_map = self._get_head(import_datas)
        results = []
        for row in import_datas:
            for i in range(1, len(row)):
                m = re.match(r'(\S+)\s+(\S+)', row[i])
                if m:
                    results += [(head_map[i][0],
                                 head_map[i][1],
                                 row[0],
                                 m.group(1),
                                 m.group(2),
                                 timetable_id,)]
        return results, import_fields

    @staticmethod
    def _read_csv(record):
        """ Returns a CSV-parsed iterator of all empty lines in the file

        :throws csv.Error: if an error is detected during CSV parsing
        :throws UnicodeDecodeError: if ``options.encoding`` is incorrect
        """
        csv_iterator = csv.reader(
            StringIO.StringIO(record))
        csv_nonempty = itertools.ifilter(None, csv_iterator)
        encoding = 'utf-8'
        return itertools.imap(
            lambda row: [item.decode(encoding) for item in row],
            csv_nonempty)

    @api.multi
    def button_import(self):
        if not self[0].timetable_id:
            self[0].timetable_id = self.env.context['timetable_id']
        if self.env['school.timetable'].browse(self[0].timetable_id).cell_ids:
            raise exceptions.Warning(_('Already Have Cells, if what redo import, please delete current cells and import again.'))
        datas = self._read_csv(base64.decodestring(self[0].data))
        data, import_fields = self._convert_import_data(datas, self[0].timetable_id)

        _logger.info('importing %d rows...', len(data))
        self.env.cr.execute('SAVEPOINT import')
        results = self.pool['school.timetable.cell'].load(self.env.cr, self.env.uid, import_fields, data, context=self.env.context)
        if results and results['messages']:
            messages = ['<p style="color:red">%s</p>' % r['message'] for r in results['messages']]
            _logger.info('Error occur during import!')
            self.env.cr.execute('ROLLBACK TO SAVEPOINT import')
            self.message = ''.join(messages)
        else:
            self.env.cr.execute('RELEASE SAVEPOINT import')
            self.message = '<p style="color: green">%s</p>' % u'成功'
            self.state = 'finish'
            _logger.info('done')

        res = self.env['ir.actions.act_window'].for_xml_id('class_import', 'action_school_timetable_import')
        res['res_id'] = self[0].id
        return res
