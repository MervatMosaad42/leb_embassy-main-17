# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContactPassport(models.Model):
    _name = 'ebs_mod.contact.passport'
    _description = "contact Passport"
    _rec_name = 'passport_no'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact')

    family_member = fields.Selection(
        string='Family Member',
        selection=[('me', 'Applicant'),
                   ('father', 'Father'),
                   ('mother', 'Mother '),
                   ('spouse', 'Spouse '),
                   ('child', 'Child ')
                   ]
    )
    travel_doc_type = fields.Selection(
        string='Travel Document Type',
        selection=[('P', 'Passport'),
                   ('TD', 'Travel Document'),
                   ('LP', 'Laisser-passer'),
                   ('O', 'Others')
                   ], default='P'
    )

    dependent = fields.Many2one(
        comodel_name='res.partner',
        string='Dependent',
        required=False
    )

    passport_no = fields.Char(
        string='Passport No',
        required=False)

    passport_place = fields.Char(
        string='Passport Place',
        required=False)
    passport_start_date = fields.Date(
        string='Passport Start Date',
        required=False)

    passport_exp_date = fields.Date(
        string='Passport Expiry Date',
        required=False)

    is_active = fields.Boolean('Active', default=False)

