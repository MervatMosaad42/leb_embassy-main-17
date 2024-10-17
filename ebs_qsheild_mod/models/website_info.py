# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AboutEmbassy(models.Model):
    _name = 'ebs_mod.about.embassy'
    _description = "About The Embassy"


    type = fields.Char(
        string='Type',
        required=True,
        translate=True)

    description = fields.Html(
        string='Description',
        required=True,
        translate=True)

    embassy_image = fields.Binary("Image")


class Communicate(models.Model):
    _name = 'ebs_mod.communicate.embassy'
    _description = "Communicate with The Embassy"

    type = fields.Char(
        string='Type',
        required=True,
        translate=True)

    email = fields.Char(
        string='Email'
    )

    phone = fields.Char(
        string='Phone'
    )


class ImportantLinks(models.Model):
    _name = 'ebs_mod.important.links'
    _description = "Important Links"

    name = fields.Char(
        string='Name',
        required=True,
        translate=True)

    link = fields.Char(
        string='Link',
        required=True
    )


class AmbassadorsNames(models.Model):
    _name = 'ebs_mod.ambassadors.names'
    _description = "Ambassadors Names"

    name = fields.Char(
        string='Ambassador Name',
        required=True,
        translate=True)

    from_date = fields.Date(
        string='From Date',
        required=True)

    to_date = fields.Date(
        string='To Date',
        required=True)

class ContactDetail(models.Model):
    _name = 'ebs_mod.contact.details'
    _description = "Contact Details"

    name = fields.Char(
        string='Type',
        required=True,
        translate=True)

    phone = fields.Char(
    string='Phone')

    fax = fields.Char(
        string='Fax')