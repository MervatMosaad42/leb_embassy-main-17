# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class AttachmentCustom(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        allowed_extensions_list = self.env['ebs.attachment.block.types'].search([]).mapped("name")
        for values in vals_list:
            if values['name'].split(".")[-1] in allowed_extensions_list:
                raise ValidationError(_("Extension not allowed"))

        return super(AttachmentCustom, self).create(vals_list)
