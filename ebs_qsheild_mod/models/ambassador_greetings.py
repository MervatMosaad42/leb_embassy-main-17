from odoo import models, fields

class AmbassadorGreetings(models.Model):
    _name = 'ambassador.greetings'
    _description = "Ambassador greetings"

    name = fields.Char(string='Title')
    date = fields.Date(string='Date')
    description = fields.Html("Text")
    active = fields.Boolean('Active')