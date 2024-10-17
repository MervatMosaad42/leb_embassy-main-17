from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class ServiceRequest(models.Model):
    _name = 'ebs_mod.service.request'
    _description = "Service Request"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'service_number'
    _order = 'date desc'

    service_number = fields.Char(string='Service Number', index=True, default="/", copy=False)
    code = fields.Char(
        string='Code',
        required=False)

    service_beneficiary = fields.Many2one(
        comodel_name='res.partner',
        string='Service Beneficiary',
        required=False
    )

    name = fields.Char(
        string='Name',
        required=False,
        default='/'
    )
    partner_document_count = fields.Integer(
        string='Contact Uploaded Documents Count',
        required=False, default=0)

    start_date = fields.Datetime(
        string='Start Date',
        required=False, readonly=True)

    end_date = fields.Datetime(
        string='End Date',
        required=False, readonly=True)

    service_type_id = fields.Many2one(
        comodel_name='ebs_mod.service.types',
        string='Service Type',
        required=True
    )

    assigned_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned To',
        domain=[('share', '=', False)]
    )

    date_assign = fields.Date(string='Assignation Date', readonly=True)

    service_code = fields.Char(
        related='service_type_id.code',
        string='Service Code',
        required=False)

    is_started = fields.Boolean(
        string='Is Started',
        required=False, default=False)

    is_mail_sent = fields.Boolean(
        string='Mail Sent',
        required=False, default=False)

    sla_min = fields.Integer(
        string='SLA - Minimum Days',
        required=False,
        related="service_type_id.sla_min", readonly=True)

    sla_max = fields.Integer(
        string='SLA - Maximum Days',
        required=False,
        related="service_type_id.sla_max", readonly=True
    )
    sla_days = fields.Integer(
        string='SLA - Days',
        required=False,
        readonly=True)
    estimated_end_date = fields.Date(
        string='Estimated End Date',
        required=False)

    bag_no = fields.Char(
        string='Diplomatic Pouch',
        required=False)

    message = fields.Html("Message",compute='_get_message')

    @api.depends('estimated_end_date')
    def _get_days_to_finish(self):
        for rec in self:
            if rec.estimated_end_date and rec.status == 'complete':
                rec.days_to_finish = self.get_date_difference(datetime.now().date(), rec.estimated_end_date, 1)
            else:
                rec.days_to_finish = 0

    days_to_finish = fields.Integer(
        string='Days to Finish',
        required=False,
        compute="_get_days_to_finish")

    related_company_ro = fields.Many2one(
        comodel_name='res.partner',
        string='Related Company',
        readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        required=True,
    )
    # Nicole added fields

    child_birth_registration = fields.Char(
        string='Child Birth Registration Number',
        required=False)
    child_birth_registration_date = fields.Date(
        string='Child Birth Certificate Date',
        required=False
    )
    spouse = fields.Many2one(
        comodel_name='res.partner',
        string='Spouse',
        required=False,
    )
    child = fields.Many2one(
        comodel_name='res.partner',
        string='Child',
        required=False,
    )
    child_birth_certificate = fields.Char(
        string='Child Birth Certificate',
        required=False)
    child_birth_certificate_date = fields.Date(
        string='Child Birth Certificate Date',
        required=False
    )
    birth_registry_number = fields.Char(
        string='Child Registry Number',
        required=False)
    birth_record_page = fields.Char(
        string='Birth Record Page',
        required=False)
    record_personal_status = fields.Char(
        string='Record Personal Status',
        required=False)
    record_transaction_number = fields.Char(
        string='Record Personal Status',
        required=False)
    starting_date = fields.Date(
        string='Starting Date',
        required=False
    )
    child_passport_number = fields.Char(
        string='Child Passport Number',
        required=False)

    spouse_passport = fields.Many2one(
        comodel_name='ebs_mod.contact.passport',
        string='Spouse Passport',
        required=False,
    )

    spouse_ikama = fields.Many2one(
        comodel_name='ebs_mod.contact.ikama',
        string='Spouse Qatar ID',
        required=False,
    )

    related_company = fields.Many2one(
        comodel_name='res.partner',
        string='Company',

    )

    date = fields.Date(
        string='Date',
        required=True
    )

    @api.depends('message_ids','activity_ids','message_follower_ids')
    def _get_message(self):
        for rec in self:
            print("...........rec.message_ids....",rec.message_ids)
            if rec.message_ids:
                author_user = self.env['res.users'].sudo().search([('partner_id','=',rec.message_ids[0].author_id.id)])
                if author_user and author_user.has_group("base.group_user"):
                    rec.message = "Replied !"
                else:
                    rec.message = "Pending !"



    def _get_arabic_req_date(self):
        date = self.date.strftime('%Y\%m\%d').replace("0", "۰").replace("1", "۱").replace("2", "۲").replace("3",
                             "۳").replace(
            "4", "٤").replace("5", "۵").replace("6", "٦").replace("7", "٧").replace("8", "۸").replace("9", "۹")
        return date

    feedback_ids = fields.One2many(
        comodel_name='ebs_mod.service.request.feedback',
        inverse_name='service_id',
        string='Feedback')

    notification_ids = fields.One2many(
        comodel_name='ebs_mod.service.request.notification',
        inverse_name='service_id',
        string='Notification')

    @api.onchange('date')
    def _date_on_change(self):
        if self.date:
            if self.env.company.disable_future_date_service:
                if self.date > date.today():
                    self.date = date.today()

    contract_id = fields.Many2one(
        comodel_name='ebs_mod.contracts',
        string='Contract',
        required=False,
        domain=[('id', '=', -1)]
    )

    partner_type = fields.Selection(
        string='Contact Type',
        selection=[
            ('company', 'Company'),
            ('emp', 'Employee'),
            ('visitor', 'Visitor'),
            ('child', 'Dependent')],
        related="partner_id.person_type"
    )
    phone = fields.Char(
        string='Phone',
        readonly=True,
        required=False,
        related="partner_id.phone")

    mobile = fields.Char(
        string='Mobile',
        required=False,
        readonly=True,
        related="partner_id.mobile")

    is_miscellaneous = fields.Boolean(
        string='Is Miscellaneous',
        required=False,
        readonly=True,
        related="partner_id.is_miscellaneous"
    )
    active = fields.Boolean(
        string='Active', default=True,
        required=False)
    email = fields.Char(
        string='Email',
        required=False,
        readonly=True,
        related="partner_id.email")

    desc = fields.Text(
        string="Description",
        required=False)
    status = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('progress', 'In Progress'),
                   ('assign', 'Assigned'),
                   ('hold', 'On Hold'),
                   ('complete', 'Completed'),
                   ('cancel', 'Canceled'),
                   ('reject', 'Rejected')],
        required=False,
        default='draft')
    status_dict = {
        'draft': 'Draft',
        'progress': 'In Progress',
        'assign': 'Assigned',
        'hold': 'On Hold',
        'complete': 'Completed',
        'reject': 'Rejected',
        'cancel': 'Canceled'
    }
    cost_center = fields.Char(
        string='Cost Center',
        required=False)

    flow_type = fields.Selection(
        string='Workflow Type',
        selection=[('o', 'Online')],
        required=False)

    service_flow_ids = fields.One2many(
        comodel_name='ebs_mod.service.request.workflow',
        inverse_name='service_request_id',
        string='Workflow',
        required=False)

    service_document_ids = fields.One2many(
        comodel_name='documents.document',
        inverse_name='service_id',
        string='Out Documents',
        required=False,
        domain="[('document_type_id.type', '=?', 'O')]"
    )

    document_in = fields.Many2many(
        comodel_name='documents.document',
        string='In Documents',
        domain="[('document_type_id.type', '=?', 'I')]"

    )

    expenses_ids = fields.One2many(
        comodel_name='ebs_mod.service.request.expenses',
        inverse_name='service_request_id',
        string='Expenses',
        required=False)
    # VISA
    purpose_of_trip = fields.Selection(
        string='Purpose of the trip',
        selection=[
            ('Family', 'Family'),
            ('Tourism', 'Tourism'),
            ('Business', 'Business'),
            ('Transit', 'Transit'),
            ('Work', 'Work'),
            ('Other', 'Other')
        ]
    )

    visa_duration = fields.Selection(
        string='Visa Duration',
        selection=[
            ('15D', ' 15  Days  '),
            ('1M', ' 1 month '),
            ('2M', '2 months'),
            ('3M', '3 months'),
            ('6M', '6 months')
        ]
    )
    nb_entries = fields.Selection(
        string='Number of Entries',
        selection=[
            ('One', 'One'),
            ('Double', 'Double'),
            ('Multiple', 'Multiple')
        ]
    )
    entry_point = fields.Selection(
        string='Point of Entry ',
        selection=[
            ('Port', 'Port'),
            ('Airport', 'Airport'),
            ('Others', 'Others')
        ]
    )
    expected_arrival_day = fields.Date(
        string='Expected Arrival day',
        required=False)
    expected_departure_day = fields.Date(
        string='Expected Departure day',
        required=False)
    visa_no = fields.Char(
        string='VISA NO ',
        required=False)
    receipt_no = fields.Char(
        string='Receipt No ',
        required=False)
    #  Passport Management
    renewal_nb = fields.Char(
        string='Renewal No ',
        required=False)
    renewal_date = fields.Date(
        string='Renewal Date',
        required=False)

    service_date = fields.Date(
        string='Service Date',
        required=False)

    # Passports information
    passport_request_period = fields.Selection(
        string='Passport Request Period',
        selection=[('one', 'One Year'),
                   ('five', 'Five Years'),
                   ]
    )

    passport_period = fields.Selection(
        string='Passport Period',
        selection=[('one', 'One Year'),
                   ('three', 'Three Years'),
                   ('five', 'Five Years'),
                   ('ten', 'Ten Years'),
                   ]
    )

    pal_doc_period = fields.Selection(
        string='Palestinian Documents Period',
        selection=[('one', 'One Year'),
                   ('three', 'Three Years'),
                   ('five', 'Five Years'),
                   ]
    )

    current_passport_type = fields.Selection(
        string='Current Passport Type',
        selection=[('E', 'Electronic '),
                   ('B', 'Biometric'),
                   ]
    )

    dhl30 = fields.Boolean(
        string='DHL',
        required=False, default=False)

    dhl25 = fields.Boolean(
        string='DHL',
        required=False, default=False)

    received_by = fields.Char(
        string='Received By',
        required=False)

    documentNo = fields.Char(
        string='Document No in Embassy',
        required=False)

    mission_name = fields.Char(
        string='Mission Name',
        required=False)

    mission_answer = fields.Char(
        string='Mission Answer',
        required=False)

    table_number = fields.Char(
        string='Table Number',
        required=False)

    order_number = fields.Char(
        string='Order Number in the daily schedule',
        required=False)

    application_date = fields.Date(
        string='Application Date',
        required=False)

    def _get_arabic_app_date(self):
        date = self.application_date
        if self.application_date and self.application_date is not None:
            date = self.application_date.strftime('%Y\%m\%d').replace("0", "۰").replace("1", "۱").replace("2", "۲").replace("3",
                                 "۳").replace(
                "4", "٤").replace("5", "۵").replace("6", "٦").replace("7", "٧").replace("8", "۸").replace("9", "۹")
        return date

    application_registration_number = fields.Char(
        string='Application Registration Number',
        required=False)

    mission_file_number = fields.Char(
        string='Mission File Number',
        required=False)

    request_type = fields.Selection(
        string='Request Type',
        selection=[('New', 'New Passport'),
                   ('Replace Missing', 'Replace Missing'),
                   ('Normal Replacement', 'Normal Replacement'),
                   ('Exceptional Replacement', 'Exceptional Replacement'),
                   ]
    )

    replacement_reason = fields.Char(
        string='Replacement Reason',
        required=False)

    applicant_profession_ar = fields.Char(
        string='Profession of the applicant  (AR)',
        required=False)

    applicant_profession_en = fields.Char(
        string='Profession of the applicant  (EN)',
        required=False)

    paid_fee = fields.Selection(
        string='Paid Fees',
        selection=[
            ('60', 'سنة واحدة،مئتان وعشرون  ريال قطري ما يعادل 90،000 ل.ل'),
            ('180', 'ثلاث سنوات،ستة مئة وستون ريال قطري ما يعادل 270،000 ل.ل'),
            ('300', 'خمس سنوات،ألف وخمس و تسعون ريال قطري ما يعادل 450،000 ل.ل'),
            ('500', 'عشر سنوات، ألفين و مئة و خمسة وثمانون ريال قطري ما يعادل 900،000 ل.ل')]
    )

    with_marital_status = fields.Boolean(
        string='I would like to write down my marital status',
        required=False, default=False)

    without_marital_status = fields.Boolean(
        string='I don\'t want to write down my marital status',
        required=False, default=False)

    with_husband_name = fields.Boolean(
        string='Do you want to add the husband\'s name to the passport?',
        required=False, default=False)

    sign_below = fields.Char(
        string='I / we are the signing below',
        required=False)

    allow_child_travel = fields.Boolean(
        string='I / We allow the minor child to travel',
        required=False, default=False)

    nb_notary_statement_ar = fields.Integer(
        string='Number of Notary Statement (Arabic)',
        required=False)
    date_notary_statement_ar = fields.Date(
        string='Date Notary Statement (Arabic)',
        required=False)

    tel_notary_statement_ar = fields.Char(
        string='Telephone Notary Statement (Arabic)',
        required=False)

    notary_fullname_ar = fields.Char(
        string='Notary Full Name (Arabic)',
        required=False)

    nb_notary_statement_en = fields.Integer(
        string='Number of Notary Statement (English)',
        required=False)

    date_notary_statement_en = fields.Date(
        string='Date Notary Statement (English)',
        required=False)

    tel_notary_statement_en = fields.Char(
        string='Telephone Notary Statement (English)',
        required=False)

    notary_fullname_en = fields.Char(
        string='Notary Full Name (English)',
        required=False)

    general_director_decision = fields.Char(
        string='General Director decision (if required)',
        required=False)

    director_decision_nb = fields.Char(
        string='General Director decision Number',
        required=False)

    director_decision_date = fields.Date(
        string='General Director decision Date',
        required=False)

    additional_documents_type = fields.Many2one(
        comodel_name='ebs_mod.document.types',
        string='Additional Document Type',
        required=False)

    additional_documents_nb = fields.Char(
        string='Additional Document Number',
        required=False)

    additional_documents_date = fields.Date(
        string='Additional Documents Date',
        required=False)

    additional_documents_exp_date = fields.Date(
        string='Additional Documents Expiry Date',
        required=False)

    consular_number = fields.Char(
        string='Consular Number',
        required=False)

    receipt_number = fields.Char(
        string='Receipt Number',
        required=False)

    release_Date = fields.Date(
        string='Release Date',
        required=False)

    # Authorization

    account_number = fields.Char(
        string='Bank Account Number',
        required=False)
    bank_name = fields.Char(
        string='Bank Name',
        required=False)
    branch = fields.Char(
        string='Branch',
        required=False)
    agent_address = fields.Char(
        string='Agent Full Address',
        required=False)

    document_count = fields.Integer(
        string='Document Count',
        required=False,
        compute="_compute_service_document_count")

    def _compute_service_document_count(self):
        for rec in self:
            rec.document_count = len(self.env['documents.document'].search([('service_id', '=', rec.id)]))



    @api.model
    def create(self, vals):
        # vals['related_company_ro'] = vals['related_company']
        if vals.get('service_number', _('/')) == _('/'):
            sequence_id = self.env.ref('ebs_qsheild_mod.service_req_no').ids
            if sequence_id:
                record_name = self.env['ir.sequence'].browse(sequence_id).next_by_id()
            else:
                record_name = '/'
            vals['service_number'] = record_name

        if self.service_beneficiary.id == '' or not self.service_beneficiary.id:
            folder = self.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)

            partner_documents = self.env['documents.document'].search([('partner_id', '=', vals['partner_id'])])
            service_type = self.env['ebs_mod.service.types'].search([('id', '=', vals['service_type_id'])])
            list_partner_docs = [doc.document_type_id.id for doc in list(partner_documents)]

            document_owner = 'me'
            for docs in list(service_type.document_types):
                if docs.id in list_partner_docs:
                    documents = self.env['documents.document'].sudo().search(
                        [('partner_id', '=', vals['partner_id']),
                         ('document_type_id', '=', docs.id)], limit=1)
                    vals['document_in'] = [(4, documents.id)]
                else:
                    documents = self.env['documents.document'].sudo().create({
                        'partner_id': vals['partner_id'],
                        'type': 'binary',
                        'document_owner': document_owner,
                        'document_type_id': docs.id,
                        'folder_id': folder.id
                    })
                    vals['document_in'] = [(4, documents.id)]
        res = super(ServiceRequest, self).create(vals)
        return res

    def write(self, vals):
        if vals.get('status', False):
            if vals['status'] != self.status:
                self.message_post(
                    body="Status changed from " + self.status_dict[self.status] + " to " + self.status_dict[
                        vals['status']] + ".")
            if vals['status'] == 'complete':
                send_mail = self.env.ref("ebs_qsheild_mod.service_completed_email_template").send_mail(self.id, email_values={'res_id': None})
            if vals['status'] == 'progress':
                service_groups = self.service_type_id.read_group_ids
                for group in service_groups:
                    users = group.users
                    for u in users:
                        email = u.login
                        self.env['mail.mail'].create({
                            'body_html': '<p>Hello ' + u.partner_id.name + ', </p><p>A new Service '
                                         + self.service_type_id.name + ' is Submitted.</p><br/><br/><p>Thank You.</p>',
                            'state': 'outgoing',
                            'email_from': u.company_id.partner_id.email,
                            'email_to': email,
                            'subject': _('New Service Submitted by ') + self.partner_id.name
                        }).send()
        if 'assigned_user_id' in vals:
            assigned_to = vals['assigned_user_id']
            status = self.status
            if assigned_to:
                if status == 'progress':
                    vals['status'] = 'assign'

        if 'bag_no' in vals:
            bag_no = vals['bag_no']
            if bag_no:
                self.env['ebs_mod.service.request.notification'].sudo().create({
                    'service_id': self.id,
                    'partner_id': self.partner_id.id,
                    'notification': 'bag',
                    'is_read': False
                })

        res = super(ServiceRequest, self).write(vals)

        return res

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban'), (False, 'tree'), (False, 'form')],
            'view_mode': 'kanban',
            'context': {
                "search_default_service_id": self.id,
                "default_service_id": self.id,
                "searchpanel_default_folder_id": False,
                "hide_contact": True,
                "hide_service": True
            },
        }

    @api.onchange('partner_id', 'date')
    def partner_company_onchange(self):
        self.contract_id = None
        self.service_type_id = None
        if self.env.context.get('default_partner_id', False):
            self.partner_id = self.env.context.get('default_partner_id')
        if self.date and self.partner_id:

            if self.partner_id.person_type == 'company':
                self.related_company_ro = self.partner_id.id
                self.related_company = self.partner_id.id
            else:
                self.related_company_ro = self.partner_id.related_company.id
                self.related_company = self.partner_id.related_company.id

            contract_list = self.env['ebs_mod.contracts'].search([
                ('contact_id', '=', self.related_company.id),
                ('start_date', '<=', self.date),
                ('end_date', '>=', self.date),
            ])
            if self.partner_id.person_type == 'company':
                return {
                    'domain': {
                        'contract_id': [('contact_id', '=', self.related_company.id),
                                        ('start_date', '<=', self.date),
                                        ('end_date', '>=', self.date), ]
                    }
                }

    def get_contact_contract_list(self, contact, contract_list):
        contact_contract_list = []
        for rec in contract_list:
            if self.check_contract_contact(rec, contact):
                contact_contract_list.append(rec.id)
        return contact_contract_list

    @api.onchange('contract_id')
    def contract_id_on_change(self):
        self.service_type_id = None
        if self.contract_id:
            if self.contract_id.service_ids:
                contact_service_list = self.get_contact_related_service_types(self.contract_id.service_ids.ids,
                                                                              self.partner_id)
                return {
                    'domain':
                        {
                            'service_type_id': [('id', 'in', contact_service_list)]
                        }
                }
            else:
                return {'warning': {'title': _('Warning'),
                                    'message': _(
                                        'Selected contract has no services for this contact type')}}

    def get_contact_related_service_types(self, service_type_ids, contact_id):
        domain = [('id', 'in', service_type_ids)]
        if contact_id.person_type == 'emp':
            domain.append(('for_employee', '=', True))
        elif contact_id.person_type == 'visitor':
            domain.append(('for_visitor', '=', True))
        elif contact_id.person_type == 'child':
            domain.append(('for_dependant', '=', True))
        else:
            domain.append(('for_company', '=', True))

        if contact_id.is_miscellaneous:
            domain.append(('for_miscellaneous', '=', True))
        else:
            domain.append(('for_not_miscellaneous', '=', True))

        services_list = self.env['ebs_mod.service.types'].search(domain)
        if len(services_list) == 0:
            return []
        else:
            return services_list.ids

    def check_contract_contact(self, contract, contact_id):
        contact_list = []
        if contact_id.person_type == 'emp':
            contact_list = contract.employee_list.ids
        elif contact_id.person_type == 'visitor':
            contact_list = contract.visitor_list.ids
        elif contact_id.person_type == 'child':
            contact_list = contract.dependant_list.ids
        if contact_id.id in contact_list:
            return True
        else:
            return False

    def request_submit(self):
        if len(self.service_flow_ids) == 0:
            self.flow_type = 'o'

        if self.code:
            code = self.code
        else:
            code = self.env['ir.sequence'].next_by_code('ebs_mod.service.request')

        year = str(self.date.year)
        month = self.date.strftime("%B")
        service_red = self.service_type_id.code or ""
        self.code = code
        self.name = service_red + "-" + month + year + "-" + code
        self.status = 'progress'

    def get_date_difference(self, start, end, jump):
        delta = timedelta(days=jump)
        start_date = start
        end_date = end
        count = 0
        while start_date < end_date:
            start_date += delta
            count += 1
        return count

    def request_cancel(self):
        for flow in self.service_flow_ids:
            flow.status = 'cancel'
        self.end_date = datetime.today()
        if self.start_date and self.end_date:
            self.sla_days = self.get_date_difference(self.start_date.date(), self.end_date.date(), 1)
        else:
            self.sla_days = 0
        self.status = 'cancel'

    def request_reject(self):
        for flow in self.service_flow_ids:
            flow.status = 'reject'
        self.end_date = datetime.today()
        if self.start_date and self.end_date:
            self.sla_days = self.get_date_difference(self.start_date.date(), self.end_date.date(), 1)
        else:
            self.sla_days = 0
        self.status = 'reject'

    def request_complete(self):
        complete = True
        if complete:
            self.end_date = datetime.today()
            if self.start_date and self.end_date:
                self.sla_days = self.get_date_difference(self.start_date.date(), self.end_date.date(), 1)
            else:
                self.sla_days = 0
            self.status = 'complete'
        else:
            raise ValidationError(_("Workflow still pending or in progress."))

    def request_hold(self):
        self.status = 'hold'

    def request_progress(self):
        self.status = 'progress'

    def request_draft(self):

        if len(self.service_flow_ids) == 0 and len(self.service_document_ids) == 0 and len(self.expenses_ids) == 0:
            self.start_date = None
            self.end_date = None
            self.status = 'draft'
        else:
            raise ValidationError(_("Delete all Related Items."))

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.service_number))
        return result

    def unlink(self):
        for rec in self:
            if len(rec.service_document_ids) != 0:
                raise ValidationError(_("Delete Related Documents"))
            for flow in rec.service_flow_ids:
                flow.unlink()
        return super(ServiceRequest, self).unlink()


class ServiceRequestExpenses(models.Model):
    _name = "ebs_mod.service.request.expenses"
    _description = "Service Request Expenses"
    _order = 'date'

    expense_type_id = fields.Many2one(
        comodel_name='ebs_mod.expense.types',
        string='Expense type',
        required=True)

    service_request_id = fields.Many2one(
        comodel_name='ebs_mod.service.request',
        string='Service Request',
        required=True)

    related_company_ro = fields.Many2one(
        comodel_name='res.partner',
        string='Related Company',
        related="service_request_id.related_company_ro"
    )
    contract_id = fields.Many2one(
        comodel_name='ebs_mod.contracts',
        string='Contract',
        related="service_request_id.contract_id"
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        related="service_request_id.partner_id"
    )

    partner_type = fields.Selection(
        string='Contact Type',
        selection=[
            ('company', 'Company'),
            ('emp', 'Employee'),
            ('visitor', 'Visitor'),
            ('child', 'Dependent')],
        related="partner_id.person_type"
    )

    desc = fields.Text(
        string="Description",
        required=False)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True)
    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
        required=True,
        default=0.0)

    date = fields.Date(
        string='Payment Date',
        required=True)



    payment_by = fields.Char(
        string='Payment By',
        required=True)


class ContactNotification(models.Model):
    _name = 'ebs_mod.service.request.notification'
    _rec_name = 'service_id'

    notification = fields.Text(string="Notification")
    service_id = fields.Many2one(
        comodel_name='ebs_mod.service.request',
        string='Service',
        required=False)

    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string='Contact',
                                 required=False,
                                 readonly=True)

    is_read = fields.Boolean(
        string='is Read',
        required=False,
        default=False)


class FeedBack(models.Model):
    _name = 'ebs_mod.service.request.feedback'
    _rec_name = 'service_id'
    rating = fields.Selection(
        [('0', 'Poor'), ('1', 'Low'), ('2', 'Normal'), ('3', 'Medium'), ('4', 'High'), ('5', 'Execellent')], 'Rating')
    comments = fields.Text(string="Comments", required=True)
    date = fields.Date("Date", default=fields.Date.today)

    service_id = fields.Many2one(
        comodel_name='ebs_mod.service.request',
        string='Service',
        required=False)

    service_type = fields.Many2one(related='service_id.service_type_id',
                                   comodel_name='ebs_mod.service.types',
                                   string='Service Type',
                                   required=False,
                                   readonly=False)

    service_contact = fields.Many2one(related='service_id.partner_id',
                                      comodel_name='res.partner',
                                      string='Contact',
                                      required=False,
                                      readonly=False)
