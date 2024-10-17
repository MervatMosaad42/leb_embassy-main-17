from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime,date


class JobVacanciesApplicant(models.Model):
    _name = 'job.vacancies.applicant'

    name = fields.Char("Name",required=True)
    family_name = fields.Char("Family Name",required=True)
    date_of_birth = fields.Date("Date Of Birth",required=True)
    passport_no = fields.Char("Passport No",required=True)
    passport_issuance_place = fields.Char("Passport Issuance Place",required=True)
    passport_issuance_date = fields.Date("Passport Issuance Date",required=True)
    passport_expiry_date = fields.Date("Passport Expiry Date",required=True)
    qid_expiry_date = fields.Date("Qid Expiry Date",required=True)
    # resident_in_doha = fields.Selection([('yes','YES'),('no','NO')],default="yes",string="Resident In Doha")
    qid = fields.Char("QID",required=True)
    resident_in_qatar = fields.Selection([('yes','YES'),('no','NO')],string="Resident In Qatar",default='yes')
    contact_email = fields.Char("Contact Email",required=True)
    contact_phone = fields.Char("Contact Phone No",required=True)
    notice_period = fields.Selection([('up to 1 month','Up To 1 Months'),('up to 2 month','Up To 2 Months'),
                                                      ('more than 2 month','More Than 2 Months')],default='up to 1 month',string="Notice Period")
    marital_status = fields.Many2one("marital.status","Marital Status",required=True)
    qtr_address = fields.Char("Address in Qatar",required=True)
    resume = fields.Text("Cv Summary",required=True)
    skills = fields.Text("Skills",required=True)
    education_info = fields.One2many("education.info",'applicant_id',string="Education Information",required=True)
    job_history = fields.One2many("job.history",'applicant_id',string="Job History",required=True)
    cover_letter = fields.Many2one('ir.attachment',"Cover Letter",required=True)
    cv_attachment = fields.Many2one('ir.attachment',"Cv Attachment",required=True)
    name_and_family = fields.Char(compute="concate_name_and_family_name",string="Name")
    job_position_applicant = fields.Char(string="Position",compute="_compute_job_position",store=True)
    degree_applicant = fields.Char(string="Degree",compute="_compute_degree",store=True)
    user_id = fields.Many2one("res.users", "User",required=True)




    @api.depends('family_name','name')
    def concate_name_and_family_name(self):
        for rec in self:
            print("..........concate_name_and_family_name...")
            rec.name_and_family = rec.name + ' ' +rec.family_name

    @api.depends('job_history.start_date','job_history.position')
    def _compute_job_position(self):
        for rec in self:
            rec.job_position_applicant = ''
            if rec.job_history:
                job_history = self.env['job.history'].search([('applicant_id','=',rec.id)],order="end_date Desc" ,limit=1)
                rec.job_position_applicant = job_history.position

    @api.depends('education_info.degree')
    def _compute_degree(self):
        for rec in self:
            rec.degree_applicant = ''
            if rec.education_info:
                education_info = self.env['education.info'].search([('applicant_id','=',rec.id)],order="id Desc" ,limit=1)
                rec.degree_applicant = education_info.degree

    @api.onchange('qid')
    def qid_onchange(self):
        for rec in self:
            if rec.qid != False and (len(rec.qid) > 11 or len(rec.qid) < 11):
                raise ValidationError(_("Qid Number must be 11 digit !"))

    @api.onchange('passport_no')
    def passport_onchange(self):
        for rec in self:
            if rec.passport_no != False:
                if (rec.passport_no[:2] == 'RL' or rec.passport_no[:2] == 'LR'):
                    pass_value = True
                else:
                    raise ValidationError(_("Passport No Should be Start with RL Or LR!"))




class JobVacanciesCompany(models.Model):
    _name = 'job.vacancies.company'

    name = fields.Char("Company Name",required=True)
    industry_id = fields.Many2one('vacancies.industry',string="Industry")
    number_of_employees = fields.Selection([('1-50','1-50'),('50-200','50-200'),('200+','200+')],"Number Of Employees",default="1-50",required=True)
    point_of_contact = fields.One2many("res.partner",'vacancy_company_id',string="Point Of Contact")
    user_id = fields.Many2one('res.users','User',required=True)

class JobVacanciesjob(models.Model):
    _name = 'job.vacancies'
    _rec_name = "position"

    position = fields.Char("Position")
    publishing_date = fields.Date("Publishing Date")
    description = fields.Text("Description")
    eductional_requirement = fields.Text("Educational Requirement")
    skills_requirement = fields.Text("Skills Requirement")
    benefits = fields.Text("Benefits")
    joining_limit = fields.Date("Joining Limit")
    vacancy_expire_date = fields.Date("Vacancy Expiry Date")
    application_link = fields.Char("Application Link")
    application_email = fields.Char("Application Email")
    work_location = fields.Char("Work Location")
    company_id = fields.Many2one('job.vacancies.company', 'Company')

class ApplicantShortlisting_Company_Shortlisting(models.Model):
    _name = 'application.company.sortlisting'

    position = fields.Many2one("job.vacancies","Position Name")
    company_name = fields.Many2one("job.vacancies.company","Company Name")
    applicant_name = fields.Many2one("job.vacancies.applicant","Applicant Name")
    company_position = fields.Char("Position")

class EducationInfo(models.Model):
    _name = 'education.info'

    applicant_id = fields.Many2one("job.vacancies.applicant")
    degree = fields.Char("Degree")
    year_from = fields.Char("Year From")
    year_to = fields.Char("Year To")
    subject = fields.Char("Subject")
    major = fields.Char("Major")
    country_id = fields.Many2one("res.country",string="Country")

class JobHistory(models.Model):
    _name = 'job.history'

    applicant_id = fields.Many2one("job.vacancies.applicant")
    position = fields.Char(string="Position")
    company_name = fields.Char(string="Company Name")
    start_date = fields.Date(string="Starting Date")
    end_date = fields.Date(string="End Date")
    description = fields.Char(string="Description")
    country_id = fields.Many2one("res.country", string="Country")
    current_position = fields.Selection([('yes','YES'),('no','NO')],default="yes",string="Current Position(yes/No)")

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    vacancy_company_id = fields.Many2one("job.vacancies.company")
    jb_position = fields.Char("Job Position")
    applicant_user_boolean = fields.Boolean()

class JobPosition(models.Model):
    _name = 'job.position'

    name = fields.Char("Name")

class MaritalStatus(models.Model):
    _name = 'marital.status'

    name = fields.Char("Name")

class VacanciesIndustry(models.Model):
    _name = 'vacancies.industry'

    name = fields.Char("Name")

