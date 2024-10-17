# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DocumentTypes(models.Model):
    _name = 'ebs_mod.document.types'
    _description = "Document Type"

    _sql_constraints = [
        ('document_type_name_unique', 'unique (name)',
         'Name must be unique !'),
    ]

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

    type = fields.Selection(
        [('I', 'In'),
         ('O', 'Out')
         ], string='Type',
        default='I')

    is_passport = fields.Boolean(
        string='is Passport',
        required=False,
        default=False)

    is_mandatory = fields.Boolean(
        string='is Mandatory for Profile Submission',
        required=False,
        default=False)

    is_required = fields.Boolean(
        string='is Required for Contact Profile',
        required=False,
        default=False)

    is_required_issue_date = fields.Boolean(
        string='is Required Issue Date',
        required=False,
        default=False)

    is_required_expiry_date = fields.Boolean(
        string='is Required Expiry Date',
        required=False,
        default=False)

    is_required_doc_no = fields.Boolean(
        string='is Required Document No',
        required=False,
        default=False)

    description = fields.Char(
        string='Description')

    for_lebanese = fields.Boolean(
        string='For Lebanese',
        required=False,
        default=False)

    for_palestinian = fields.Boolean(
        string='For Palestinian',
        required=False,
        default=False)