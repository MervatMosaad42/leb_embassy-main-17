from odoo import api, fields, models, _


class HrJobInherit(models.Model):
    _inherit = 'hr.job'

    enroll_attachment_required = fields.Boolean(
        string='Attachment Required For Enroll'
    )
