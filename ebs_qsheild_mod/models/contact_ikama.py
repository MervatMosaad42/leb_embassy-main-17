# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContactIkama(models.Model):
    _name = 'ebs_mod.contact.ikama'
    _description = "contact Ikama"
    _rec_name = 'ikama_no'

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

    dependent = fields.Many2one(
        comodel_name='res.partner',
        string='Dependent',
        required=False
    )

    ikama_no = fields.Char(
        string='QID',
        required=False)

    ikama_issue_date = fields.Date(
        string='Ikama Issue Date',
        required=False)
    ikama_enddate = fields.Date(
        string='QID End Date',
        required=False)

    guarantor = fields.Char(
        string='Sponsor',
        required=False)

    occupation = fields.Char(
        string='Occupation',
        required=False)

    is_active = fields.Boolean('Active', default=False)

