from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EbsEnrollRequests(models.Model):
    _name = 'ebs.enroll.requests'
    _description = 'Ebs Enroll Requests'

    name = fields.Char(
        string='Name',
        required=True
    )

    type = fields.Selection(
        selection=[('new', 'New'), ('update', 'Update'), ('delete', 'Delete'), ('show', 'Show'), ('hide', 'Hide')],
        string='Type'
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )

    cr_number = fields.Char(
        string='Commercial Reg Number'
    )

    industry_id = fields.Many2one(
        comodel_name='res.partner.industry',
        string='Industry'
    )

    phone = fields.Char(
        string='Phone'
    )

    email = fields.Char(
        string='Email'
    )

    website = fields.Char(
        string='Website'
    )

    status = fields.Selection(
        selection=[('submitted', 'Submitted'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')],
        string='Status',
        default='submitted'
    )

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today
    )

    reject_reason = fields.Text(
        string='Reject Reason'
    )

    address_ids = fields.One2many(
        comodel_name='ebs_mod.contact.address',
        inverse_name='enroll_request_id',
        string='Address',
    )

    social_media_ids = fields.One2many(
        comodel_name='ebs.partner.socialmedia',
        inverse_name='enroll_request_id',
        string='Address',
    )

    user_partner_id = fields.Many2one(
        related='create_uid.partner_id',
        string='User Partner'
    )

    contact_type = fields.Selection(
        selection=[('person', 'Individual'), ('company', 'Company')]
    )

    job_position = fields.Many2one(
        comodel_name='hr.job',
        string='Job Position'
    )

    authorization_letter = fields.Binary(
        string='Authorization Letter'
    )

    copy_of_crp = fields.Binary(
        string='Copy Of CRP'
    )

    identification = fields.Binary(
        string='Identification'
    )

    permission_letter = fields.Binary(
        string='Permission To Practice'
    )

    _sql_constraints = [
        ('enroll_request_cr_number_unique', 'Check(1=1)',
         'Commercial Reg Number must be unique !')
    ]

    def approve_request(self):
        if self.type == 'show':
            self.partner_id.display_on_portal = True
            self.partner_id.function = self.job_position.name
        elif self.type == 'hide':
            self.partner_id.display_on_portal = False
        elif self.type == 'new':
            enroll_id = self.env['res.partner'].search([('cr_number', '=', self.cr_number)])
            if enroll_id and self.cr_number:
                raise UserError("Commercial Reg Number must be unique !")
            new_partner_vals = {
                'name': self.name,
                'first_name_en': self.name,
                'cr_number': self.cr_number,
                'industry_id': self.industry_id.id,
                'phone': self.phone,
                'email': self.email,
                'website': self.website,
                'function': self.job_position.name,
                'company_type': self.contact_type,
                'first_Nationality': 'leb',
                'display_on_portal': True,
                'parent_id': self.create_uid.partner_id.id,
                'address_ids': [(6, 0, self.address_ids.ids)],
                'social_media_ids': [(6, 0, self.social_media_ids.ids)]
            }
            new_partner_id = self.env['res.partner'].create(new_partner_vals)
            new_partner_id.request_progress()
        elif self.type == 'delete':
            self.partner_id.active = False
        elif self.type == 'update':
            partner_vals = {}
            if self.name:
                partner_vals.update({'name': self.name})
            if self.cr_number:
                partner_vals.update({'cr_number': self.cr_number})
            if self.industry_id:
                partner_vals.update({'industry_id': self.industry_id.id})
            if self.phone:
                partner_vals.update({'phone': self.phone})
            if self.email:
                partner_vals.update({'email': self.email})
            if self.website:
                partner_vals.update({'website': self.website})
            partner_vals.update({'address_ids': [(6, 0, self.address_ids.ids)]})
            self.partner_id.write(partner_vals)
        self.status = 'confirmed'
