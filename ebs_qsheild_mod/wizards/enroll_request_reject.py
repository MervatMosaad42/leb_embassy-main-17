# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EnrollRequestRejectWizard(models.TransientModel):
    _name = 'enroll.request.reject.wizard'
    _description = 'Enroll Request Reject Wizard'

    name = fields.Text(
        string='Reason',
        required=True
    )

    enroll_request_id = fields.Many2one(
        comodel_name='ebs.enroll.requests',
        string='Enroll Request'
    )

    def confirm_button(self):
        self.enroll_request_id.reject_reason = self.name
        self.enroll_request_id.status = 'rejected'
