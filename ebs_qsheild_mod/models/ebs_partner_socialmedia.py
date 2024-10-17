from odoo import models, fields, api, _


class EbsPartnerSocialMedia(models.Model):
    _name = 'ebs.partner.socialmedia'
    _description = 'Ebs Partner Social Media'

    name = fields.Char(
        string='Name',
        required=True
    )

    type_id = fields.Many2one(
        comodel_name='ebs.socialmedia.types',
        string='Type',
        required=1
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )

    enroll_request_id = fields.Many2one(
        comodel_name='ebs.enroll.requests',
        string='Enroll Request'
    )


class EbsSocialMediaTypes(models.Model):
    _name = 'ebs.socialmedia.types'
    _description = 'Ebs Social Media Types'

    name = fields.Char(
        string='Name',
        required=True
    )
