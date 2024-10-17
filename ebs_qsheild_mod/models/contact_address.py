# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContactAddress(models.Model):
    _name = 'ebs_mod.contact.address'
    _description = "contact Address"

    contract_id = fields.Many2one(
        comodel_name='ebs_mod.contracts',
        string='Contract'
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact')

    type = fields.Selection(
        [('Lebanon', 'Lebanon'),
         ('Qatar', 'Qatar'),
         ('Company', 'Company'),

         ], string='Address Type',
        default='Lebanon')

    owned = fields.Boolean(
        string='Owned Apartment',
        required=False)

    pobox = fields.Char(
        string='PO. Box',
        required=False)

    email = fields.Char(
        string='email',
        required=False)

    street = fields.Char(
        string='Street',
        required=False)
    street2 = fields.Char(
        string='Street 2',
        required=False)

    region = fields.Many2one(
        comodel_name='ebs_mod.country.region',
        string='Region',
        required=False)

    kaza = fields.Many2one(
        comodel_name='ebs_mod.country.kaza',
        string='kaza',
        required=False)

    town = fields.Char(
        string='Town',
        required=False)

    district = fields.Char(
        string='District',
        required=False)

    zip = fields.Char(
        string='Zip',
        required=False)
    city = fields.Char(
        string='City',
        required=False)
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]")

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        ondelete='restrict')

    building = fields.Char(
        string='Building',
        required=False)
    mojama3 = fields.Char(
        string='Compound',
        required=False)
    floor = fields.Char(
        string='Floor',
        required=False)
    flat = fields.Char(
        string='Flat',
        required=False)

    qatar_region = fields.Char(
        string='Qatar Region',
        required=False)

    company_name = fields.Char(
        string='Company Name',
        required=False)

    job_position = fields.Char(
        string='Job Position',
        required=False)

    phoneNumber = fields.Char(
        string='Phone Number',
        required=False)

    mobile = fields.Char(
        string='Mobile',
        required=False)

    address_start = fields.Date(
        string='Address Start Date',
        required=False)

    is_active = fields.Boolean('Active', default=False)

    enroll_request_id = fields.Many2one(
        comodel_name='ebs.enroll.requests',
        string='Enroll Request'
    )
