# -*- coding: utf-8 -*-


from odoo import models, fields, api, tools, _


class AttachmentBlock(models.Model):
    _name = 'ebs.attachment.block.types'
    _description = 'Attachment Types'

    name = fields.Char(
        string='Extension',
        required=True)
