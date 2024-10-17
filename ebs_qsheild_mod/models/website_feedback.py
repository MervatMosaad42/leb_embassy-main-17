from odoo import models, fields, api, _

class FeedbackWebsite(models.Model):
    _name = 'feedback.feedback'

    name = fields.Char("Name")
    description = fields.Char("Description")
    rating = fields.Selection(
        [ ('0','Poor'),('1', 'Bad'), ('2', 'Not Bad'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Execellent')], 'Rating')
    email = fields.Char("Email")
    comments = fields.Char("Commnets",required=True)
