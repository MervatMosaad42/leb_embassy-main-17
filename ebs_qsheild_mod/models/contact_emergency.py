# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContactEmergency(models.Model):
    _name = 'ebs_mod.contact.emergency'
    _description = "contact Emergency"

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact')

    emergency_full_name = fields.Char(
        string='Emergency Full Name',
        required=False)

    emergency_phone_number = fields.Char(
        string='Emergency Phone Number',
        required=False)

    emergency_full_name_leb = fields.Char(
        string='Full Name of the Closest Relatives in Lebanon',
        required=False)

    emergency_phone_number_leb = fields.Char(
        string='Phone Number of the Closest Relatives in Lebanon',
        required=False)

    is_active = fields.Boolean('Active', default=False)

