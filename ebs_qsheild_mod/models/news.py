# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class News(models.Model):
    _name = 'ebs_mod.news'
    _description = "News"

    name = fields.Char(string="Description",translate=True)
    date = fields.Date(
        string='Date',
    )
    active = fields.Boolean(
        string='Active', default=True,
        required=False)