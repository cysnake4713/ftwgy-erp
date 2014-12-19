# coding=utf-8
__author__ = 'cysnake4713'

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Subject(models.Model):
    _name = 'school.subject'

    name = fields.Char('Name', required=True)

    _sql_constraints = [('school_subject_unique', 'unique(name)', _('name must be unique !'))]


class Class(models.Model):
    _name = 'school.classroom'

    name = fields.Char('Name', required=True)

    _sql_constraints = [('school_classroom_unique', 'unique(name)', _('name must be unique !'))]


class Semester(models.Model):
    _name = 'school.semester'
    _order = 'end_date desc'

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        name = u'%s (%s - %s)'
        date_convert = self._fields['start_date'].convert_to_display_name
        for record in self:
            result.append((record.id, name % (record.name, date_convert(record.start_date), date_convert(record.end_date))))
        return result

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_date_period(self):

        if self.end_date < self.start_date:
            raise Warning(_('End Date cannot be set before Start Date.'))

        result = self.env['school.semester'].search(['|', '|',
                                                     '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                     '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date),
                                                     '&', ('start_date', '>=', self.start_date), ('end_date', '<=', self.end_date),
                                                     ('id', '!=', self.id)])
        if len(result):
            raise Warning(_('Date period have overlapping'))

