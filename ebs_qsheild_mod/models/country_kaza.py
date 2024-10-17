# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CountryKaza(models.Model):
    _name = 'ebs_mod.country.kaza'
    _description = "Country Kaza"

    code = fields.Char(
        string='Code',
        required=True)

    name = fields.Char(
        string='Name (Arabic)',
        required=True)
    name_en = fields.Char(
        string='Name (English)',
        required=False)

    def _get_name(self):
        locale = self._context.get('lang') or 'en_US'
        # ar_001 for arabic

        if locale == 'en_US':
            name = self.name_en or self.name
        else:
            name = self.name or ''
        return name

    def name_get(self):
        res = []
        for service in self:
            name = service._get_name()
            res.append((service.id, name))
        return res

    region_id = fields.Many2one(
        comodel_name='ebs_mod.country.region',
        string='Region',
        required=False)
