# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request


class ContactCustom(models.Model):
    _inherit = 'res.partner'
    _parent_name = 'parent_id'

    ref = fields.Char(string='Reference', index=True, default="New", copy=False)

    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable",
                                                     domain="[('account_type', '=', 'asset_receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=False,
                                                     default=None)

    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Account Payable",
                                                  domain="[('account_type', '=', 'liability_payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=False,
                                                  default=None)
    status = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('progress', 'In Progress'),
                   ('reject', 'Rejected'),
                   ('confirm', 'Confirmed')],
        required=False,
        default='draft', copy=False, store=True)

    archive_number = fields.Integer('Archive Number')

    def request_reject(self):
        if self.email:
            ctx = {}
            ctx['subject'] = 'Application Rejected'
            ctx['email_from'] = self.env.user.company_id.email
            ctx['email_to'] = self.email
            ctx['author_id'] = self.env.user.partner_id.id
            # self.env['mail.mail'].create(mail_values).sudo().send()
            self.env.ref("ebs_qsheild_mod.reject_email").sudo().with_context(ctx).send_mail(self.id, email_values={'res_id':None})
            self.status = 'reject'
        else:
            raise ValidationError(_("Please enter email address."))

    def request_confirm(self):
        ctx = {}
        ctx['subject'] = 'Application Confirm'
        ctx['email_from'] = self.env.user.company_id.email
        ctx['email_to'] = self.email
        ctx['author_id'] = self.env.user.partner_id.id
        if self.status == 'progress':
            if self.email:
                self.env.ref("ebs_qsheild_mod.confirm_email").sudo().with_context(ctx).send_mail(self.id,email_values={'res_id':None})
                self.status = 'confirm'
            else:
                raise ValidationError(_("Please enter email address."))
        elif self.status == 'reject':
            if self.email:
                self.env.ref("ebs_qsheild_mod.confirm_email").sudo().with_context(ctx).send_mail(self.id, email_values={'res_id':None})
                self.status = 'confirm'
            else:
                raise ValidationError(_("Please enter email address."))
        else:
            raise ValidationError(_("Workflow still pending or in progress."))

    def request_progress(self):
        self.status = 'progress'

    firstName = fields.Char(
        string='First Name (Arabic)',
        required=False, copy=False)

    middleName = fields.Char(
        string='Middle Name (Arabic)',
        required=False, copy=False)

    lastName = fields.Char(
        string='Last Name (Arabic)',
        required=False, copy=False)

    motherFullName = fields.Char(
        string='Mother Full Name (Arabic)',
        required=False)

    placeOfBirth = fields.Char(
        string='Place of Birth (Arabic)',
        required=False)

    first_name_en = fields.Char(
        string='First Name (English)',
        required=False, copy=False)

    middle_name_en = fields.Char(
        string='Middle Name (English)',
        required=False, copy=False)

    last_name_en = fields.Char(
        string='Last Name (English)',
        required=False, copy=False)

    mother_full_name_en = fields.Char(
        string='Mother Full Name (English)',
        required=False)

    place_of_birth_en = fields.Char(
        string='Place of Birth (English)',
        required=False)

    housemaid_name = fields.Char(
        string='Housemaid Name',
        required=False)
    degree = fields.Char(
        string='Degree',
        required=False)
    university = fields.Char(
        string='University',
        required=False)

    # Added for Passport info

    father_fullname = fields.Char(
        string='Father Full Name (Arabic)',
        required=False)

    father_fullname_en = fields.Char(
        string='Father Full Name (English)',
        required=False)

    father_place_of_birth = fields.Char(
        string='Father Place of Birth',
        required=False)

    father_date_of_birth = fields.Date(
        string='Father Date of Birth',
        required=False)

    father_file_no = fields.Char(
        string='Father File No',
        required=False)
    father_stati_no = fields.Char(
        string='Father Stati No',
        required=False)
    father_registered_with = fields.Char(
        string='Father Registered With',
        required=False)

    mother_place_of_birth = fields.Char(
        string='Mother Place of Birth',
        required=False)

    mother_date_of_birth = fields.Date(
        string='Mother Date of Birth',
        required=False)

    mother_first_nationality = fields.Char(
        string='Mother First Nationality',
        required=False)

    mother_file_no = fields.Char(
        string='Mother File No',
        required=False)
    mother_stati_no = fields.Char(
        string='Mother Stati No',
        required=False)

    mother_registered_with = fields.Char(
        string='Mother Registered With',
        required=False)

    birth_certificate_nb = fields.Char(
        string='Birth Certificate Number',
        required=False)

    birth_certificate_date = fields.Date(
        string='Birth Certificate Date',
        required=False)

    # End
    # Religion
    religion = fields.Many2one(
        comodel_name='ebs_mod.contact.religion',
        string='Religion/Sect',
        required=False)

    father_religion = fields.Many2one(
        comodel_name='ebs_mod.contact.religion',
        string='Father Religion/Sect',
        required=False)

    mother_religion = fields.Many2one(
        comodel_name='ebs_mod.contact.religion',
        string='Mother Religion/Sect',
        required=False)

    kazaBirth = fields.Many2one(
        comodel_name='ebs_mod.country.kaza',
        string='Kaza',
        required=False)

    sejelNo = fields.Char(
        string='Registry Number',
        required=False)

    sejel_place = fields.Char(
        string='Registry Place',
        required=False)

    maritalStatus = fields.Selection(
        string='Marital Status',
        selection=[('Single', 'Single'),
                   ('Married', 'Married'),
                   ('Widowed', 'Widowed '),
                   ('Divorced', 'Divorced '),
                   ]
    )

    id_no = fields.Char(
        string='Lebanese ID Number',
        required=False)

    file_no = fields.Char(
        string='File No',
        required=False)
    stati_no = fields.Char(
        string='Stati No',
        required=False)
    registered_with = fields.Char(
        string='Registered With',
        required=False)

    parent_id = fields.Many2one('res.partner', string='Related Contact', index=True)
    date_stop_renew = fields.Date(
        string='Do Not Renew After',
        required=False)
    is_miscellaneous = fields.Boolean(
        string='Is Miscellaneous',
        required=False, default=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female')],
        required=False)
    person_type = fields.Selection(
        string='Person Type',
        selection=[('emp', 'Individual'),
                   ('child', 'Dependent')],
        default='emp'
    )

    first_Nationality = fields.Selection(
        string='Nationality',
        selection=[
            ('leb', 'Lebanese'),
            ('pal', 'Palestinian'),
            ('other', 'Other')
        ], default=lambda self: self.env.context.get('default_natio')
    )

    dependent_type = fields.Selection(
        string='Family Member',
        selection=[
            ('spouse', 'Spouse/Husband'),
            ('child', 'Child'),
        ],
    )

    date_join = fields.Date(
        string='join Date',
        required=False)

    date_termination = fields.Date(
        string='Termination Date',
        required=False)

    other_nationality = fields.Many2one(
        comodel_name='res.country',
        string='Nationality',
        required=False)

    nationality = fields.Many2one(
        comodel_name='res.country',
        string='Second Nationality',
        required=False)

    qatar_id_doc = fields.Many2one(
        comodel_name='documents.document',
        string='Qatar ID Document',
        required=False
    )

    qatarfirstvisit_date = fields.Date(
        string='Qatar First Visit Date',
        required=False)
    company_name = fields.Char(
        string='Company Name',
        required=False)

    marriage_place = fields.Char(
        string='Marriage Place',
        required=False)

    marriage_date = fields.Date(
        string='Marriage Date',
        required=False)

    schoolName = fields.Char(
        string='School Name',
        required=False)

    qatar_id = fields.Char(
        string='Qatar ID',
        required=False)

    passport_no = fields.Char(
        string='Passport No',
        required=False)

    qatarid_exp_date = fields.Date(
        string='Qatar ID Expiry Date',
        # related='qatar_id_doc.expiry_date',
        required=False)

    computer_card_doc = fields.Many2one(
        comodel_name='documents.document',
        string='Computer Card Document',
        required=False
    )

    # computer_card_number = fields.Char(
    #     string='Computer Card Number',
    #     required=False)
    comp_card_exp_date = fields.Date(
        string='Computer Card Expiry Date', related='computer_card_doc.expiry_date',
        required=False)

    cr_number_doc = fields.Many2one(
        comodel_name='documents.document',
        string='CR Number Document',
        required=False
    )

    # cr_number = fields.Char(
    #     string='CR Number',
    #     required=False)
    cr_exp_date = fields.Date(
        string='CR Expiry Date', related='cr_number_doc.expiry_date',
        required=False)

    trade_licence_doc = fields.Many2one(
        comodel_name='documents.document',
        string='Trade Licence Document',
        required=False
    )

    # trade_licence_number = fields.Char(
    #     string='Trade Licence Number',
    #     required=False)
    trade_licence_date = fields.Date(
        string='Trade Licence Expiry Date', related='trade_licence_doc.expiry_date',
        required=False)

    account_manager = fields.Many2one(
        comodel_name='hr.employee',
        string='Account Manager',
        required=False)

    company_visitors = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Related Visitors',
        required=False, domain=[('person_type', '=', 'visitor')]
    )

    company_employees = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Related Employees',
        required=False, domain=[('person_type', '=', 'emp')]
    )

    employee_dependants = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Related Dependants',
        required=False
    )

    passport_doc = fields.Many2one(
        comodel_name='documents.document',
        string='Passport Document',
        required=False
    )

    contact_emergency = fields.One2many(
        comodel_name='ebs_mod.contact.emergency',
        inverse_name='partner_id',
        string='Emergency',
        required=False)

    contact_passports = fields.One2many(
        comodel_name='ebs_mod.contact.passport',
        inverse_name='partner_id',
        string='Passports',
        required=False)

    contact_ikama = fields.One2many(
        comodel_name='ebs_mod.contact.ikama',
        inverse_name='partner_id',
        string='Ikama',
        required=False)

    sponsor_for = fields.One2many(
        comodel_name='res.partner',
        inverse_name='sponsor',
        string='Sponsor For',
        required=False, readonly=True
    )
    contracts = fields.One2many(
        comodel_name='ebs_mod.contracts',
        inverse_name='contact_id',
        string='Contracts',
        required=False)

    document_o2m = fields.One2many(
        comodel_name='documents.document',
        inverse_name='partner_id',
        string='Related Documents',
        required=False)

    service_ids = fields.One2many(
        comodel_name='ebs_mod.service.request',
        inverse_name='partner_id',
        string='Services',
        required=False)

    address_ids = fields.One2many(
        comodel_name='ebs_mod.contact.address',
        inverse_name='partner_id',
        string='Address',
        required=False)

    def _get_service_count(self):
        for rec in self:
            rec.service_count = len(rec.service_ids)

    service_count = fields.Integer(
        string='Services Count',
        required=False,
        compute="_get_service_count")

    display_on_portal = fields.Boolean(
        string='Display On Portal'
    )

    social_media_ids = fields.One2many(
        comodel_name='ebs.partner.socialmedia',
        inverse_name='partner_id',
        string='Social Media'
    )

    cr_number = fields.Char(
        string='Commercial Reg Number'
    )
    
    enroll_request_ids = fields.One2many(
        comodel_name='ebs.enroll.requests',
        inverse_name='user_partner_id'
    )

    _sql_constraints = [
        ('person_type_name_parent_unique', 'unique (person_type, parent_id,name, ref)',
         'The combination of Type, Related Contact and Name must be unique !'),
    ]

    # document_o2m_archived = fields.One2many(
    #     comodel_name='documents.document',
    #     inverse_name='partner_id',
    #     string='Related Documents Archived',
    #     required=False, compute="_get_archived_documents",
    # )
    #
    # def _get_archived_documents(self):
    #     for rec in self:
    #         ids = []
    #         # for doc in self.env['documents.document'].with_context(active_test=False).search(
    #         #         [('partner_id', '=', rec.id), ('active', '=', False)]):
    #         #     ids.append(doc.id)
    #         rec.document_o2m_archived = self.env['documents.document'].with_context(active_test=False).search(
    #             [('partner_id', '=', rec.id), ('active', '=', False)])

    # def sponsor_domain(self):
    #     if self.person_type == 'company':
    #         return [('person_type', '=', 'company')]
    #     if self.person_type == 'emp' or self.person_type == 'visitor':
    #         return [('person_type', '=', 'company')]
    #     if self.person_type == 'child':
    #         return ['|', ('person_type', '=', 'emp'), ('person_type', '=', 'company')]

    @api.depends('parent_id')
    def _sponsor_default(self):
        if self.person_type == 'company':
            return self.id
        if self.person_type in ('emp', 'visitor'):
            return self.parent_id.id
        if self.person_type == 'child':
            self.sponsor = self.parent_id.parent_id.id
        return None

    @api.depends('parent_id')
    def _sponsor_compute(self):
        for rec in self:
            if rec.person_type == 'company':
                if 'default_sponsor' in rec._context:
                    if rec._context['default_sponsor']:
                        rec.sponsor = rec._context['default_sponsor']
                else:
                    rec.sponsor = rec.id
            if rec.person_type == 'visitor' or rec.person_type == 'emp':
                if 'default_sponsor' in rec._context:
                    if rec._context['default_sponsor']:
                        rec.sponsor = rec._context['default_sponsor']
                else:
                    rec.sponsor = rec.parent_id.id
            if rec.person_type == 'child':
                if 'default_sponsor' in rec._context:
                    if rec._context['default_sponsor']:
                        rec.sponsor = rec._context['default_sponsor']
                else:
                    rec.sponsor = rec.parent_id.sponsor.id

    sponsor = fields.Many2one(
        comodel_name='res.partner',
        string='Sponsor',
        required=False,
        readonly=False,
        default=_sponsor_default,
        # compute='_sponsor_compute', store=True,
        domain=[('person_type', '=', 'company')])

    @api.depends('parent_id')
    def _get_related_company(self):
        for rec in self:
            if rec.person_type == 'child':
                rec.related_company = rec.parent_id.parent_id.id
            if rec.person_type in ('emp', 'visitor'):
                rec.related_company = rec.parent_id.id

    related_company = fields.Many2one(
        comodel_name='res.partner',
        string='Related Company',
        required=False,
        store=True,
        compute='_get_related_company')

    dependants = fields.One2many(
        comodel_name='res.partner',
        inverse_name='related_company',
        string='Dependants',
        required=False, readonly=True)

    contact_relation_type_id = fields.Many2one(
        comodel_name='ebs_mod.contact.relation.type',
        string='Relation Type',
        required=False)

    payment_ids = fields.One2many(
        comodel_name='ebs_mod.contact.payment',
        inverse_name='partner_id',
        string='Payments',
        required=False)

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    @api.depends_context('show_address', 'show_address_only', 'show_email', 'html_format', 'show_vat')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None, html_format=None, show_vat=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            if partner.person_type:
                partner.display_name = partner.name
            else:
                partner.display_name = names.get(partner.id)

    @api.onchange('person_type')
    def _person_type_change(self):
        if self.person_type == 'company':
            self.company_type = 'company'
        else:
            self.company_type = 'person'

    @api.onchange('firstName', 'lastName', 'middleName')
    def _onchange_name(self):
        if self.firstName and self.lastName and self.middleName:
            self.name = self.firstName + ' ' + self.middleName + ' ' + self.lastName
        elif self.firstName and self.lastName:
            self.name = self.firstName + ' ' + self.lastName
        elif self.firstName:
            self.name = self.firstName

    # return {
    #     'domain': {
    #         'sponsor': self.sponsor_domain()
    #     }
    # }

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            sequence_id = self.env.ref('ebs_qsheild_mod.res_partner_ref_no').ids
            if sequence_id:
                record_name = self.env['ir.sequence'].browse(sequence_id).next_by_id()
            else:
                record_name = 'New'
            vals['ref'] = record_name

        res = super(ContactCustom, self).create(vals)

        if res:
            if not res.country_id:
                res.country_id = 126
            bool_create_sponsor = False
            if 'sponsor' not in vals:
                bool_create_sponsor = True
            else:
                if not vals['sponsor']:
                    bool_create_sponsor = True
            if bool_create_sponsor:
                if 'person_type' in vals:
                    if vals['person_type'] == 'company':
                        res.sponsor = res.id
                    if vals['person_type'] in ('visitor', 'emp'):
                        if res.parent_id:
                            res.sponsor = res.parent_id.id
                    if vals['person_type'] == 'child':
                        if res.parent_id.sponsor:
                            res.sponsor = res.parent_id.sponsor.id

            required_documents = self.env['ebs_mod.document.types'].sudo().search([('is_required', '=', True),
                                                                                   ('for_lebanese', '=', True)])
            folder = self.env['documents.folder'].sudo().search([('is_default_folder', '=', True)], limit=1)
            for docs in required_documents:
                documents = self.env['documents.document'].sudo().create({
                    'name': '/',
                    'partner_id': res.id,
                    'type': 'binary',
                    'document_type_id': docs.id,
                    'folder_id': folder.id,
                })

            vals['first_Nationality'] = 'leb'
        print("//////////\n\n\n\n\n...create..", self._context)
        if self._context.get('partner_create', False):
            add_list = []
            for rec in res:
                if not rec.address_ids:
                    raise ValidationError("please make address for Qatar and Lebanon")
                for add in rec.address_ids:
                    add_list.append(add.type)
                if not all(item in add_list for item in ["Lebanon", "Qatar"]):
                    raise ValidationError("please make address for Qatar and Lebanon..")
        return res

    def write(self, vals):
        for partner in self:
            if vals.get('parent_id', False):
                new_res = self.env['res.partner'].browse(vals['parent_id'])
                # for rec in partner.employee_dependants:
                #     rec.related_company = new_res.id
                #     rec.sponsor = new_res.sponsor.id
                # partner.message_post(
                #     body="Related contact changed from '" + partner.parent_id.name + "' to '" + new_res.name + "'")

            if 'active' in vals:
                partner.contact_archive_onchange(vals.get('active'))

            if self.first_Nationality and vals.get('first_Nationality', False):
                if vals.get('first_Nationality', False) != self.first_Nationality:
                    partner.document_o2m.sudo().unlink()

            required_documents = False
            isLebanese = False
            isPalestinian = False

            if vals.get('first_Nationality', False) == 'leb':
                isLebanese = True
                required_documents = self.env['ebs_mod.document.types'].sudo().search([('is_required', '=', True),
                                                                                       ('for_lebanese', '=',
                                                                                        isLebanese)])
            elif vals.get('first_Nationality', False) == 'pal':
                isPalestinian = True
                required_documents = self.env['ebs_mod.document.types'].sudo().search([('is_required', '=', True),
                                                                                       ('for_palestinian', '=',
                                                                                        isPalestinian
                                                                                        )])
            # by mervat
            # else:
            #     required_documents = request.env['ebs_mod.document.types'].sudo().search([('is_required', '=', True),
            #                                                                               ('for_lebanese', '=', False),
            #                                                                               ('for_palestinian', '=',
            #                                                                                False)])

            folder = self.env['documents.folder'].sudo().search([('is_default_folder', '=', True)], limit=1)
            partner_docs = [doc.document_type_id for doc in list(partner.document_o2m)]

            if required_documents and partner.first_Nationality is not None and partner.first_Nationality != '':
                for docs in required_documents:
                    if docs not in partner_docs:
                        documents = self.env['documents.document'].sudo().create({
                            'name': '/',
                            'partner_id': partner.id,
                            'type': 'binary',
                            'document_type_id': docs.id,
                            'folder_id': folder.id
                        })
                print("....write........rec.....", partner)
                print("............rec.address_ids....", partner.address_ids)
        res = super(ContactCustom, self).write(vals)
        print(",.......\n\n\n\n\n\n ......", self._context)
        if self._context.get('partner_create', False):
            add_list = []
            for rec in self:
                if not rec.address_ids:
                    raise ValidationError("please make address for Qatar and Lebanon")
                for add in rec.address_ids:
                    add_list.append(add.type)
                if not all(item in add_list for item in ["Lebanon", "Qatar"]):
                    raise ValidationError("please make address for Qatar and Lebanon..")
        return res

    def contact_archive_onchange(self, active):
        self.contact_document_archive(active)
        related_contacts_list = self.env['res.partner'].search(
            [('parent_id', '=', self.id), ('active', '=', (not active))])
        for rec in related_contacts_list:
            rec.active = active

    def contact_document_archive(self, active):
        document_list = self.env['documents.document'].search(
            [('partner_id', '=', self.id), ('active', '=', (not active))])
        for rec in document_list:
            rec.active = active

    def _get_name(self):
        if self.person_type:
            return self.name
        else:
            return super(ContactCustom, self)._get_name()

    def _get_arabic_date(self):

        date = self.date.strftime('%Y\%m\%d').replace("0", "۰").replace("1", "۱").replace("2", "۲").replace("3",
                                                                                                            "۳").replace(
            "4", "٤").replace("5", "۵").replace("6", "٦").replace("7", "٧").replace("8", "۸").replace("9", "۹")
        return date

    def _get_arabic_date_employee(self, date_emp):
        print("=========================dateeeeeeeeempppppppppp", date_emp)
        if date_emp:
            date = date_emp.strftime('%Y\%m\%d').replace("0", "۰").replace("1", "۱").replace("2", "۲").replace("3",
                                                                                                               "۳").replace(
                "4", "٤").replace("5", "۵").replace("6", "٦").replace("7", "٧").replace("8", "۸").replace("9", "۹")
            return date
        else:
            return date_emp

    def _get_arabic_nationality(self):
        nationality = ''
        if self.first_Nationality == 'leb':
            nationality = 'لبنانية'
        elif self.first_Nationality == 'pal':
            nationality = 'فلسطينية'
        else:
            nationality = self.env['res.country'].with_context(lang='ar_001').search(
                [('id', '=', self.nationality.id)]).name

        return nationality

    def unlink(self):
        for rec in self:
            if rec.person_type == 'company':
                if len(rec.company_visitors) > 0 or len(rec.company_employees) > 0:
                    raise ValidationError(_("Cannot delete, check linked items"))
            if rec.person_type == 'emp':
                if len(rec.employee_dependants) > 0:
                    raise ValidationError(_("Cannot delete, check linked items"))

            for doc in rec.document_o2m:
                doc.unlink()
            super(ContactCustom, rec).unlink()

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        # return values in result, as this method is used by _fields_sync()
        if not self.parent_id:
            return
        result = {}
        partner = self._origin

    def _fields_sync(self, values):
        self._children_sync(values)

    def _get_second_nationality_passport_info(self, res_partner):
        doc_type_passport = self.env['ebs_mod.document.types'].search([('name', '=', 'صورة عن الجواز الاجنبي')])
        second_nationality_passport = False
        if doc_type_passport:
            second_nationality_passport = res_partner.document_o2m.filtered(
                lambda doc: doc.document_type_id.id == doc_type_passport.id)
        return second_nationality_passport and second_nationality_passport[0]
