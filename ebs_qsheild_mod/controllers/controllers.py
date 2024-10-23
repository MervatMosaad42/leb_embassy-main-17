# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, content_disposition
import os
from datetime import timedelta
import base64
import logging
import werkzeug
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from datetime import datetime,date
from odoo.exceptions import UserError
from odoo.http import request, route
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.web import Home
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class Website(Home):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        # mySeparator = "       "
        # news_id = mySeparator.join(request.env['ebs_mod.news'].sudo().search([]).mapped('name')).rjust(20)
        if request.env.user.has_group('base.group_public'):
            public_user = True

        else:
            public_user =False
        list=[]
        mob_first=[]
        mob_sec=[]
        mob_third=[]
        mob_fourth=[]
        mob_fifth=[]
        mob_six=[]
        first_two=[]
        second_two=[]
        thire_two=[]
        announcement_id = request.env['circulars.page'].sudo().search([('page_active','=',True)],order="id desc", limit=6)
        for ann in announcement_id:
            list.append(ann.id)
        if len(list) > 0:
            first_two.append(list[0])
            mob_first.append(list[0])
        if len(list) > 1:
            first_two.append(list[1])
            mob_sec.append(list[1])
        if len(list) > 2:
            second_two.append(list[2])
            mob_third.append(list[2])
        if len(list) > 3:
            second_two.append(list[3])
            mob_fourth.append(list[3])
        if len(list) > 4:
            thire_two.append(list[4])
            mob_fifth.append(list[4])
        if len(list) > 5:
            thire_two.append(list[5])
            mob_six.append(list[5])
        first = request.env['circulars.page'].browse(tuple(first_two))
        second = request.env['circulars.page'].browse(tuple(second_two))
        third = request.env['circulars.page'].browse(tuple(thire_two))
        mobile_first_view = request.env['circulars.page'].browse(tuple(mob_first))
        mobile_second_view = request.env['circulars.page'].browse(tuple(mob_sec))
        mobile_third_view = request.env['circulars.page'].browse(tuple(mob_third))
        mobile_fourth_view = request.env['circulars.page'].browse(tuple(mob_fourth))
        mobile_fifth_view = request.env['circulars.page'].browse(tuple(mob_fifth))
        mobile_six_view = request.env['circulars.page'].browse(tuple(mob_six))
        return request.render('ebs_qsheild_mod.homepage_template',{'announcement_id':announcement_id,'first':first,'second':second,'third':third,'list':list,
                                                                   'mobile_first_view':mobile_first_view,
                                                                   'mobile_second_view':mobile_second_view,
                                                                   'mobile_third_view':mobile_third_view,
                                                                   'mobile_fourth_view':mobile_fourth_view,
                                                                   'mobile_fifth_view':mobile_fifth_view,
                                                                   'mobile_six_view':mobile_six_view,
                                                                   'public_user':public_user
                                                                   })


class QshieldController(http.Controller):

    def binary_content(self, id, env=None, field='datas', share_id=None, share_token=None,
                       download=False, unique=False, filename_field='name'):
        env = env or request.env
        record = env['documents.document'].browse(int(id))
        filehash = None

        if share_id:
            share = env['documents.share'].sudo().browse(int(share_id))
            record = share._get_documents_and_check_access(share_token, [int(id)], operation='read')
        if not record:
            return (404, [], None)

        # check access right
        try:
            last_update = record['write_date']
        except AccessError:
            return (404, [], None)

        mimetype = False
        if record.type == 'url' and record.url:
            module_resource_path = record.url
            filename = os.path.basename(module_resource_path)
            status = 301
            content = module_resource_path
        else:
            status, content, filename, mimetype, filehash = env['ir.http']._binary_record_content(
                record, field=field, filename=None, filename_field=filename_field,
                default_mimetype='application/octet-stream')
        status, headers, content = env['ir.http']._binary_set_headers(
            status, content, filename, mimetype, unique, filehash=filehash, download=download)

        return status, headers, content

    def _get_file_response(self, id, field='datas', share_id=None, share_token=None):
        """
        returns the http response to download one file.

        """

        status, headers, content = self.binary_content(
            id, field=field, share_id=share_id, share_token=share_token, download=False)

        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)

        return response

    @http.route(['/documents/content/preview/<int:id>'], type='http', auth='user')
    def documents_content(self, id):
        return self._get_file_response(id)

#     @http.route('/ebs_qsheild_mod/ebs_qsheild_mod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ebs_qsheild_mod/ebs_qsheild_mod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ebs_qsheild_mod.listing', {
#             'root': '/ebs_qsheild_mod/ebs_qsheild_mod',
#             'objects': http.request.env['ebs_qsheild_mod.ebs_qsheild_mod'].search([]),
#         })

#     @http.route('/ebs_qsheild_mod/ebs_qsheild_mod/objects/<model("ebs_qsheild_mod.ebs_qsheild_mod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ebs_qsheild_mod.object', {
#             'object': obj
#         })
#
class ImportantLink(http.Controller):
    @http.route('/importantlink', type='http', auth='public',website='True')
    def Importantlink(self):
        return http.request.render('ebs_qsheild_mod.important_link_webpage', {})




class AboutEmbassy(http.Controller):
    @http.route('/aboutembassy', type='http', auth='public',website='True')
    def aboutembassy(self):
        print("------------aboutembassy------------")
        return http.request.render('ebs_qsheild_mod.aboutembassy_webpage', {})


class AmbassadorList(http.Controller):
    @http.route('/previuosambassador', type='http', auth='public',website='True')
    def Ambassadorlist(self):
        return http.request.render('ebs_qsheild_mod.ambassador_list_webpage', {})


class CurrentAmbassador(http.Controller):
    @http.route('/currentambassador', type='http', auth='public',website='True')
    def Ambassadorlist(self):
        return http.request.render('ebs_qsheild_mod.current_ambassador_list_webpage', {})

class portal_report_data(http.Controller):
    @http.route('/portal/report/data/print/', type='json', website='True', auth='public')
    def portal_report_data(self,**kw):
        print("......kw...*************************************...",kw)
        print("......kw.get('other_nationality')...*************************************...",kw.get('other_nationality'))
        # spouse_name = request.env['res.partner'].sudo().browse(int(kw.get('spouse_name')))
        print("...kw.get('portal_service_request_spouse_id').....",kw.get('portal_service_request_spouse_id'))
        # service_request_id_new = request.env['res.partner'].sudo().browse(int(kw.get('service_request_id_new')))
        # portal_service_request_spouse_id = request.env['res.partner'].sudo().browse(int(kw.get('portal_service_request_spouse_id')))
        # print(".......portal_service_request_spouse_id......",portal_service_request_spouse_id)
        print("......kw.get('leb_description')....",kw.get('leb_description'))
        print("......kw.get('qtr_description')....",kw.get('qtr_description'))
        # dict(request._fields['first_Nationality'].selection).get(portal_service_request_spouse_id.first_Nationality)
        values = {
            # 'service_request_id_new':service_request_id_new,
            'company':request.env.user.company_id,
            'archive_no':kw.get('archive_no'),
            'leb_description':kw.get('leb_description'),
            'qtr_description':kw.get('qtr_description'),
            'person_name':kw.get('person_name'),
            'Nationality':kw.get("Nationality"),
            'qid':kw.get('qid'),
            # 'spouse_name':(spouse_name.firstName if spouse_name.firstName else '') +' ' + (spouse_name.middleName if spouse_name.middleName else '' )+' '+ (spouse_name.lastName if spouse_name.lastName else ''),
            'spouse_name':kw.get('spouse_name'),
            'nationality_of_spouse':kw.get('nationality_of_spouse'),

            'sponsor_name':kw.get('sponsor_name'),
            'sponsor_mobile':kw.get('sponsor_mobile'),
            'sponsor_fax':kw.get('sponsor_fax'),
            'pobox':kw.get('pobox'),
            'education':kw.get('education'),
            'school_university':kw.get('school_university'),
            'certificateissue_date':kw.get('certificateissue_date'),
            'labnon_street':kw.get('labnon_street'),
            'labnon_owned':kw.get('labnon_owned'),
            'labnon_mobile':kw.get('labnon_mobile'),
            'labnon_floor':kw.get('labnon_floor'),
            'qatar_street':kw.get('qatar_street'),
            'qatar_buliding':kw.get('qatar_buliding'),
            'qatar_floor':kw.get('qatar_floor'),
            'qatar_mobile':kw.get('qatar_mobile'),
            'emergency_name':kw.get('emergency_name'),
            'emergency_contact':kw.get('emergency_contact'),
            'portal_report_date':kw.get('portal_report_date'),
        }
        if kw.get('other_nationality'):
            other_nationality_obj = request.env['res.country'].sudo().browse(int(kw.get('other_nationality')))
            values.update({'other_nationality':other_nationality_obj.name,})

        pdf = request.env.ref('ebs_qsheild_mod.portal_report_embassy').sudo().render_qweb_pdf([int(kw.get('service_request_id'))],data=values)[0]

        attachment = request.env['ir.attachment'].sudo().create({
            'name': 'portal report',
            'datas': base64.b64encode(pdf),
            'type': 'binary',
            'public': True,
            'res_model': 'ebs_mod.service.request',
            'res_id': int(kw.get('service_request_id')),
            'mimetype': 'application/pdf',
        })

        print("/...attachment..",attachment)
        return attachment.id


    @http.route('/job/vacancies', type='http', auth='user', website='True')
    def job_vacancies(self):
        user_type =''
        if request.env.user.has_group('ebs_qsheild_mod.company_profile_grp'):
            user_type='company_profile'
        if request.env.user.partner_id.person_type == 'emp':
            user_type = 'applicant_profile'
        print("............user_type===========\b\n\n\n\n\n\=====",user_type)
        print("............partner===========\b\n\n\n\n\n\=====",request.env.user.partner_id)
        return http.request.render('ebs_qsheild_mod.job_vacancies_template', {'user_type':user_type})

    @http.route('/save/jobs/record', type='http', auth='public', website='True')
    def save_jobs_rec(self):
        save_jobs_data = request.env['application.company.sortlisting'].sudo().search([('applicant_name.user_id','=',request.env.user.id),(('position.vacancy_expire_date','>=',date.today()))])
        return http.request.render('ebs_qsheild_mod.job_vacancies_save_jobs_template', {'save_jobs_data':save_jobs_data,})

    @http.route('/job/vacancies/record', type='http', auth='public', website='True')
    def job_vacancies_rec(self,**post):
        job_vacancies_id = request.env['job.vacancies'].sudo().search([('vacancy_expire_date', '>=', date.today())])
        print(".......job_vacancies_id............", job_vacancies_id)
        if request.env.user.has_group('ebs_qsheild_mod.company_profile_grp'):
            job_vacancies_id = request.env['job.vacancies'].sudo().search([('vacancy_expire_date','>=',date.today()),('company_id.user_id','=',request.env.user.id)])
            print("...111....job_vacancies_id............",job_vacancies_id)
        user_type = ''
        if request.env.user.has_group('ebs_qsheild_mod.company_profile_grp'):
            user_type='company_profile'
            search_product = ''
        if request.env.user.partner_id.person_type == 'emp':
            user_type = 'applicant_profile'
            search_product = ''
        print("......job_vacancies_id...",job_vacancies_id)
        if post.get('search'):
            job_vacancies_id = request.env['job.vacancies'].sudo().search([('vacancy_expire_date', '>=', date.today()),'|','|',('position','ilike',post.get('search')) , ('description','ilike',post.get('search')),('skills_requirement','ilike',post.get('search'))])
            if request.env.user.has_group('ebs_qsheild_mod.company_profile_grp'):
                job_vacancies_id = request.env['job.vacancies'].sudo().search(
                    [('company_id.user_id','=',request.env.user.id),('vacancy_expire_date', '>=', date.today()), '|', '|', ('position', 'ilike', post.get('search')),
                     ('description', 'ilike', post.get('search')), ('skills_requirement', 'ilike', post.get('search'))])

            search_product = post.get('search')
        return http.request.render('ebs_qsheild_mod.job_vacancies_rec_template', {'job_vacancies_id':job_vacancies_id,'user_type':user_type,'search_product':search_product})

    @http.route('/job/vacancies/<int:vacancy_id>', type='http', auth='public', website='True')
    def job_vacancies_form(self,vacancy_id):
        if vacancy_id:
            job_vacancies_id = request.env['job.vacancies'].sudo().browse(vacancy_id)
        return http.request.render('ebs_qsheild_mod.job_vacancies_form_template', {'job_vacancies_id':job_vacancies_id if job_vacancies_id else False,})

    @http.route('/job/position/<int:position_id>', type='http', auth='public', website='True')
    def job_position_rec(self,position_id):
        if position_id:
            job_vacancies_id = request.env['job.vacancies'].sudo().browse(position_id)
        return http.request.render('ebs_qsheild_mod.job_position_form_template', {'job_vacancies_id':job_vacancies_id if job_vacancies_id else False,})

    # @http.route('/job/seekers/<int:seekres_id>', type='http', auth='public', website='True')
    # def job_vacancies_seekers_form(self, seekres_id):
    #     if seekres_id:
    #         job_seekers_id = request.env['job.vacancies.applicant'].sudo().browse(seekres_id)
    #     return http.request.render('ebs_qsheild_mod.job_vacancies_seekeres_form_template',
    #                                {'applicant_id': job_seekers_id if job_seekers_id else False, })



    @http.route(['/job/applicant/account/','/job/seekers/<int:seekers_id>','/job/applicant/<int:applicant_id>'], type='http', auth='public', website='True')
    def job_vacancies_applicant(self,**post):
        print("......post.......",post)
        applicant_id = request.env['job.vacancies.applicant'].sudo().search([('user_id','=',request.env.user.id)],limit=1)
        account = "applicant_profile"
        if post.get('seekers_id'):
            account = "job_Seekers"
            applicant_id = request.env['job.vacancies.applicant'].sudo().browse(int(post.get('seekers_id')))
        if post.get('applicant_id'):
            account = "saved_applicant"
            applicant_id = request.env['job.vacancies.applicant'].sudo().browse(int(post.get('applicant_id')))
        return http.request.render('ebs_qsheild_mod.job_vacancies_applicant_template',{'applicant_id':applicant_id,'account_type':account})

    @http.route('/job/company/account/', type='http', auth='public', website='True')
    def job_vacancies_company(self,**post):
        job_company_id = request.env['job.vacancies.company'].sudo().search([('user_id','=',request.env.user.id)],limit=1)
        return http.request.render('ebs_qsheild_mod.job_company_portal_profile_template',{'job_company_id':job_company_id})

    @http.route('/applicant/profile/info/', type='http', auth='public', website='True')
    def applicant_data_create(self,**kw):
        print(".........kw.................====================.",kw)
        if kw.get('applicant_profile_name'):
            request.env['job.vacancies.applicant'].sudo().browse(int(kw.get('applicant_profile_name'))).write({
                'name': kw.get('applicant_name'),
                'family_name': kw.get('applicant_family_name'),
                'date_of_birth': (
                    datetime.strptime(kw.get('applicant_date_of_birth'), DEFAULT_SERVER_DATE_FORMAT) if kw.get(
                        'applicant_date_of_birth') else ''),
                'passport_no': kw.get('applicant_passport_no'),
                'passport_issuance_place': kw.get('applicant_passport_issuance'),
                'passport_issuance_date': kw.get('applicant_passport_issuance_date'),
                'passport_expiry_date': kw.get('applicant_passport_expiry_date'),
                'qid_expiry_date': kw.get('applicant_qid_expiry_date'),
                'qid': kw.get('contact_qid'),
                'resident_in_qatar': kw.get('applicant_resident_in_qatar'),
                'contact_email': kw.get('contact_email'),
                'contact_phone': kw.get('contact_phone_no'),
                'notice_period': kw.get('contact_notice_period'),
                'marital_status': (
                    int(kw.get('contact_marital_status')) if kw.get('contact_marital_status') else False),
                'qtr_address': kw.get('contact_address_qatar'),
                'resume': kw.get('contact_cv_summary'),
                'skills': kw.get('contact_skills'),
                # 'cover_letter': attachment_cover_id.id,
                # 'cv_attachment': attachment_cv_id.id,
                'user_id': request.env.user.id,


            })

        else:
            attachment_cover_id = []
            Attachments = request.env['ir.attachment']
            if kw.get('applicant_cover_letter', False):

                for attach in request.httprequest.files.getlist('applicant_cover_letter'):
                    attachment_cover_id = Attachments.create({'name': attach.filename,
                                   'datas': base64.encodebytes(attach.read()),
                                   })
            if kw.get('applicant_cv_attachment', False):
                for attach in request.httprequest.files.getlist('applicant_cv_attachment'):
                    attachment_cv_id = Attachments.create({'name': attach.filename,
                                   'datas': base64.encodebytes(attach.read()),
                                   })

            request.env['job.vacancies.applicant'].sudo().create({
                'name': kw.get('applicant_name'),
                'family_name':kw.get('applicant_family_name'),
                'date_of_birth':(datetime.strptime(kw.get('applicant_date_of_birth'), DEFAULT_SERVER_DATE_FORMAT) if kw.get('applicant_date_of_birth') else ''),
                'passport_no':kw.get('applicant_passport_no'),
                'passport_issuance_place':kw.get('applicant_passport_issuance'),
                'passport_issuance_date':kw.get('applicant_passport_issuance_date'),
                'passport_expiry_date':kw.get('applicant_passport_expiry_date'),
                'qid_expiry_date':kw.get('applicant_qid_expiry_date'),
                'qid':kw.get('contact_qid'),
                'resident_in_qatar':kw.get('applicant_resident_in_qatar'),
                'contact_email':kw.get('contact_email'),
                'contact_phone':kw.get('contact_phone_no'),
                'notice_period':kw.get('contact_notice_period'),
                'marital_status':(int(kw.get('contact_marital_status')) if kw.get('contact_marital_status') else False) ,
                'qtr_address':kw.get('contact_address_qatar'),
                'resume':kw.get('contact_cv_summary'),
                'skills':kw.get('contact_skills'),
                'cover_letter':attachment_cover_id.id,
                'cv_attachment':attachment_cv_id.id,
                'user_id':request.env.user.id,
            })
        return request.redirect('/job/applicant/account/')



    @http.route('/applicant/education/info/', type='json', auth='public', website='True')
    def applicant_eudction_info_create(self, **kw):
        applicant_id = request.env['job.vacancies.applicant'].sudo().search([('user_id','=',request.env.user.id)])
        # print("..........kw...........",kw)
        print("kw.get('cover_letter').......",kw.get('cover_letter'))
        if not applicant_id:
            Attachments = request.env['ir.attachment']
            if kw.get('cover_letter'):
                res = kw.get('cover_letter').split(",")
                attachment_cover_id = Attachments.sudo().create({
                    'name': "Applicant cover letter",
                    'type': 'binary',
                    'datas': res[1],
                    'res_model': 'job.vacancies.applicant',
                    # 'res_id': int(kw.get('expense_id'))
                })
                print("..........attachment_cover_id.......",attachment_cover_id)
            if kw.get('cv_attachment'):
                res = kw.get('cv_attachment').split(",")
                attachment_cv_id = Attachments.sudo().create({
                    'name': "Applicant cv attachment",
                    'type': 'binary',
                    'datas': res[1],
                    'res_model': 'job.vacancies.applicant',
                    # 'res_id': int(kw.get('expense_id'))
                })
                print("..........attachment_cv_id.......",attachment_cv_id)

            request.env['job.vacancies.applicant'].sudo().create({
                'name': kw.get('name'),
                'family_name':kw.get('family_name'),
                'date_of_birth':kw.get('date_of_birth'),
                'passport_no':kw.get('pass_no'),
                'passport_issuance_place':kw.get('pass_issu_place'),
                'passport_issuance_date':kw.get('pass_issu_date'),
                'passport_expiry_date':kw.get('pass_expiry_date'),
                'qid_expiry_date':kw.get('qid_expiry_date'),
                'qid':kw.get('qid'),
                'resident_in_qatar':kw.get('resident_in_qatar'),
                'contact_email':kw.get('contact_email'),
                'contact_phone':kw.get('contact_phone'),
                'notice_period':kw.get('notice_period'),
                'marital_status':(int(kw.get('marital_status')) if kw.get('marital_status') else False) ,
                'qtr_address':kw.get('add_qatar'),
                'resume':kw.get('cv_summary'),
                'skills':kw.get('skills'),
                'cover_letter':attachment_cover_id.id,
                'cv_attachment':attachment_cv_id.id,
                'user_id':request.env.user.id,
                'education_info': [(0, 0, {
                    'degree': (kw.get('degree') if kw.get('degree') else ''),
                    'year_from': (kw.get('year_from') if kw.get('year_from') else ''),
                    'year_to': (kw.get('year_to') if kw.get('year_to') else ''),
                    'subject': (kw.get('subject') if kw.get('subject') else ''),
                    'major': (kw.get('major') if kw.get('major') else ''),
                    'country_id': (kw.get('country') if kw.get('country') else False),
            })]
            })

        else:
            applicant_id.sudo().write({
                'education_info': [(0, 0, {
                    'degree': (kw.get('degree') if kw.get('degree') else ''),
                    'year_from': (kw.get('year_from') if kw.get('year_from') else ''),
                    'year_to': (kw.get('year_to') if kw.get('year_to') else ''),
                    'subject': (kw.get('subject') if kw.get('subject') else ''),
                    'major': (kw.get('major') if kw.get('major') else ''),
                    'country_id':(kw.get('country') if kw.get('country') else False),
                })]
            })
        return True


    @http.route('/applicant/job/history/info/', type='json', auth='public', website='True')
    def applicant_job_history_create(self, **kw):
        applicant_id = request.env['job.vacancies.applicant'].sudo().search([('user_id','=',request.env.user.id)],limit=1)
        # print("..........kw...........",kw)
        if not applicant_id:
            Attachments = request.env['ir.attachment']
            if kw.get('cover_letter'):
                res = kw.get('cover_letter').split(",")
                print("...1.....res............",res)
                attachment_cover_id = Attachments.sudo().create({
                    'name': "Applicant cover letter",
                    'type': 'binary',
                    'datas': res[1],
                    'res_model': 'job.vacancies.applicant',
                    # 'res_id': int(kw.get('expense_id'))
                })
            if kw.get('cv_attachment'):
                res = kw.get('cv_attachment').split(",")
                attachment_cv_id = Attachments.sudo().create({
                    'name': "Applicant cv attachment",
                    'type': 'binary',
                    'datas': res[1],
                    'res_model': 'job.vacancies.applicant',
                    # 'res_id': int(kw.get('expense_id'))
                })

            request.env['job.vacancies.applicant'].sudo().create({
                'name': kw.get('name'),
                'family_name':kw.get('family_name'),
                'date_of_birth':kw.get('date_of_birth'),
                'passport_no':kw.get('pass_no'),
                'passport_issuance_place':kw.get('pass_issu_place'),
                'passport_issuance_date':kw.get('pass_issu_date'),
                'passport_expiry_date':kw.get('pass_expiry_date'),
                'qid_expiry_date':kw.get('qid_expiry_date'),
                'qid':kw.get('qid'),
                'resident_in_qatar':kw.get('resident_in_qatar'),
                'contact_email':kw.get('contact_email'),
                'contact_phone':kw.get('contact_phone'),
                'notice_period':kw.get('notice_period'),
                'marital_status':(int(kw.get('marital_status')) if kw.get('marital_status') else False) ,
                'qtr_address':kw.get('add_qatar'),
                'resume':kw.get('cv_summary'),
                'skills':kw.get('skills'),
                'cover_letter':attachment_cover_id.id,
                'cv_attachment':attachment_cv_id.id,
                'user_id':request.env.user.id,
                'job_history': [(0, 0, {
                    'position': (kw.get('position') if kw.get('position') else ''),
                    'company_name': (kw.get('company_name') if kw.get('company_name') else ''),
                    'start_date': (datetime.strptime(kw.get('start_date'), DEFAULT_SERVER_DATE_FORMAT) if kw.get('start_date') else ''),
                    'end_date': (datetime.strptime(kw.get('end_date'), DEFAULT_SERVER_DATE_FORMAT) if kw.get('end_date') else ''),
                    'description': (kw.get('description') if kw.get('description') else ''),
                    'country_id': (kw.get('country') if kw.get('country') else False),
                    'current_position': (kw.get('current_position') if kw.get('current_position') else False),
                })]
            })
        else:
            applicant_id.sudo().write({
                'job_history': [(0, 0, {
                    'position': (kw.get('position') if kw.get('position') else ''),
                    'company_name': (kw.get('company_name') if kw.get('company_name') else ''),
                    'start_date': (datetime.strptime(kw.get('start_date'), DEFAULT_SERVER_DATE_FORMAT) if kw.get('start_date') else ''),
                    'end_date': (datetime.strptime(kw.get('end_date'), DEFAULT_SERVER_DATE_FORMAT) if kw.get('end_date') else ''),
                    'description': (kw.get('description') if kw.get('description') else ''),
                    'country_id':(kw.get('country') if kw.get('country') else False),
                    'current_position':(kw.get('current_position') if kw.get('current_position') else 'yes'),
                })]
            })
        return True

    @http.route('/applicant/edit/education/info/', type='json', auth='public', website='True')
    def applicant_edit_eudction_info_create(self, **kw):
        if kw.get('education_rec_id'):
            eductaion_info_id = request.env['education.info'].sudo().browse(int(kw.get('education_rec_id')))
            eductaion_info_id.sudo().write({
                    'degree': (kw.get('degree') if kw.get('degree') else ''),
                    'year_from': (kw.get('year_from') if kw.get('year_from') else ''),
                    'year_to': (kw.get('year_to') if kw.get('year_to') else ''),
                    'subject': (kw.get('subject') if kw.get('subject') else ''),
                    'major': (kw.get('major') if kw.get('major') else ''),
                    'country_id': (kw.get('country') if kw.get('country') else False),
            })
        return True

    @http.route('/applicant/edit/job/history/', type='json', auth='public', website='True')
    def applicant_edit_job_history_create(self, **kw):
        if kw.get('job_rec_id'):
            job_rec_id = request.env['job.history'].sudo().browse(int(kw.get('job_rec_id')))
            job_rec_id.sudo().write({
                'position': (kw.get('position') if kw.get('position') else ''),
                'company_name': (kw.get('company_name') if kw.get('company_name') else ''),
                'start_date': (kw.get('start_date') if kw.get('start_date') else ''),
                'end_date': (kw.get('end_date') if kw.get('end_date') else ''),
                'description': (kw.get('description') if kw.get('description') else ''),
                'country_id': (kw.get('country') if kw.get('country') else False),
                'current_position': (kw.get('current_position') if kw.get('current_position') else 'yes'),
            })
        return True

    @http.route('/vacancies/form/record/', type='http', auth='public', website='True')
    def vacancies_form_record(self, **kw):
        if kw.get('job_vacancies_rec_id'):
            job_vac_rec_id = request.env['job.vacancies'].sudo().browse(int(kw.get('job_vacancies_rec_id')))
            job_vac_rec_id.sudo().write({
                'position': (kw.get('position_name') if kw.get('position_name') else ''),
                'publishing_date': (kw.get('publishing_date') if kw.get('publishing_date') else ''),
                'description': (kw.get('vacancies_description') if kw.get('vacancies_description') else ''),
                'eductional_requirement': (kw.get('vacancies_eductional_requirement') if kw.get('vacancies_eductional_requirement') else ''),
                'skills_requirement': (kw.get('vacancies_skills_requirement') if kw.get('vacancies_skills_requirement') else ''),
                'benefits': (kw.get('vacancies_benefits') if kw.get('vacancies_benefits') else False),
                'joining_limit': (kw.get('vacancies_joining_limit') if kw.get('vacancies_joining_limit') else ''),
                'vacancy_expire_date': (kw.get('vacancies_vacancy_expire_date') if kw.get('vacancies_vacancy_expire_date') else ''),
                'application_link': (kw.get('vacancies_application_link') if kw.get('vacancies_application_link') else ''),
                'application_email': (kw.get('vacancies_application_email') if kw.get('vacancies_application_email') else ''),
                'work_location': (kw.get('vacancies_work_location') if kw.get('vacancies_work_location') else ''),
            })
        return request.redirect('/job/vacancies/%s'%(job_vac_rec_id.id))

    @http.route('/vacancies/save/job/', type='json', auth='public', website='True')
    def vacancies_save_job(self, **kw):
        if request.env.user.partner_id.person_type == 'emp':
            print("..........kw.get('job_vac_id').......",kw.get('job_vac_id'))
            if kw.get('job_vac_id'):
                vacancy_id = request.env['job.vacancies'].sudo().browse(int(kw.get('job_vac_id')))
                applicant_id = request.env['job.vacancies.applicant'].sudo().search([('user_id', '=', request.env.user.id)],limit=1)
                print("........applicant_id.......",applicant_id)
                job_vac_sort_list_rec_id = request.env['application.company.sortlisting'].search([('position','=',int(kw.get('job_vac_id'))),('applicant_name','=',applicant_id.id)])
                print("....job_vac_sort_list_rec_id..........",job_vac_sort_list_rec_id)
                if not job_vac_sort_list_rec_id and applicant_id:
                    request.env['application.company.sortlisting'].sudo().create({
                        'position': int(kw.get('job_vac_id')),
                        'company_name':vacancy_id.company_id.id,
                        'applicant_name':applicant_id.id,
                    })
                    return True
        # else:
        #     if request.env.user.has_group('ebs_qsheild_mod.company_profile_grp'):
        #         if kw.get('job_vac_id'):
        #             applicant_id = request.env['job.vacancies.applicant'].sudo().search([('user_id', '=', request.env.user.id)])
        #             job_vac_sort_list_rec_id = request.env['application.company.sortlisting'].search([('position','=',int(kw.get('job_vac_id'))),('applicant_name','=',applicant_id.id)])
        #             job_vac_rec_id = request.env['job.vacancies'].sudo().browse(int(kw.get('job_vac_id')))
        #             vac_company_id = request.env['job.vacancies.company'].sudo().create({
        #                 'name': request.env.user.partner_id.name,
        #                 'user_id':request.env.user.id
        #             })
        #             job_vac_rec_id.write({
        #                 'company_id':vac_company_id.id
        #             })
        #             if not job_vac_sort_list_rec_id:
        #                 request.env['application.company.sortlisting'].sudo().create({
        #                     'position': int(kw.get('job_vac_id')),
        #                     'company_name':vac_company_id.id,
        #                     # 'applicant_name':applicant_id.id,
        #                 })
                return False


    @http.route('/company/point/of/contact/line/', type='json', auth='public', website='True')
    def company_point_of_contact_create(self, **kw):
        if kw.get('company_rec'):
            company_id = request.env['job.vacancies.company'].sudo().browse(int(kw.get('company_rec')))
            if company_id:
                company_id.sudo().write({
                    'point_of_contact': [(0, 0, {
                        'name': (kw.get('name') if kw.get('name') else ''),
                        'jb_position': (kw.get('position') if kw.get('position') else ''),
                        'email': (kw.get('email') if kw.get('email') else ''),
                        'phone': (kw.get('phone') if kw.get('phone') else ''),
                    })]
                })
            # print("..........kw...........",kw)
        else:
            request.env['job.vacancies.company'].sudo().create({
            'name': kw.get('company_name')if kw.get('company_name') else '',
            'industry_id': int(kw.get('industry_id')if kw.get('industry_id') else False),
            'number_of_employees': (kw.get('number_of_employees')if kw.get('number_of_employees') else '1-50'),
            'user_id': request.env.user.id,
            'point_of_contact': [(0, 0, {
                'name': (kw.get('name') if kw.get('name') else ''),
                'jb_position': (kw.get('position') if kw.get('position') else ''),
                'email': (kw.get('email') if kw.get('email') else ''),
                'phone': (kw.get('phone') if kw.get('phone') else ''),
            })]
            })

        return True

    @http.route('/company/edit/point/of/contact/', type='json', auth='public', website='True')
    def company_edit_point_of_contact(self, **kw):
        if kw.get('company_point_of_contact_id'):
            contact_rec_id = request.env['res.partner'].sudo().browse(int(kw.get('company_point_of_contact_id')))
            contact_rec_id.sudo().write({
                'name': (kw.get('name') if kw.get('name') else ''),
                'jb_position': (kw.get('position') if kw.get('position') else ''),
                'email': (kw.get('email') if kw.get('email') else ''),
                'phone': (kw.get('phone') if kw.get('phone') else ''),
            })
        return True

    @http.route('/company/job/vacancies/create/', type='json', auth='public', website='True')
    def company_job_vacancies_create(self, **kw):
        print(".......kw......",kw)
        publish_date = datetime.strptime(kw.get('publising_date'), DEFAULT_SERVER_DATE_FORMAT)
        joining_limit_date = datetime.strptime(kw.get('joining_limit'), DEFAULT_SERVER_DATE_FORMAT)
        expiry_date = datetime.strptime(kw.get('expiry_date'), DEFAULT_SERVER_DATE_FORMAT)
        company_id = request.env['job.vacancies.company'].sudo().search([('user_id','=',request.env.user.id)])
        if not company_id:
            company_id = request.env['job.vacancies.company'].sudo().create({
                'name':request.env.user.partner_id.name,
                'user_id':request.env.user.id
            })
        request.env['job.vacancies'].sudo().create({
            'position': (kw.get('position_name') if kw.get('position_name') else ''),
            'publishing_date': publish_date,
            'description': (kw.get('description') if kw.get('description') else ''),
            'eductional_requirement': (kw.get('educational_requirement') if kw.get('educational_requirement') else ''),
            'skills_requirement': (kw.get('skills_requirement') if kw.get('skills_requirement') else ''),
            'benefits': (kw.get('benefits') if kw.get('benefits') else False),
            'joining_limit':joining_limit_date ,
            'vacancy_expire_date': expiry_date,
            'application_link': (kw.get('application_link') if kw.get('application_link') else ''),
            'application_email': (kw.get('application_mail') if kw.get('application_mail') else ''),
            'work_location': (kw.get('work_location') if kw.get('work_location') else ''),
            'company_id':company_id.id,
        })
        return True


    @http.route(['/company/job/seekers/'], type='http', auth='public', website='True')
    def company_job_seekers(self, **kw):
        print(".......kw......",kw)
        if kw.get('search_remove_input'):
            kw.get('search') == False
        applicant_ids = request.env['job.vacancies.applicant'].sudo().search([])
        search_product = ''
        resident_in_qatar = ''
        if kw.get('search'):
            applicant_ids = request.env['job.vacancies.applicant'].sudo().search(['|','|','|',('resume','ilike',kw.get('search')) , ('skills','ilike',kw.get('search')),('degree_applicant','ilike',kw.get('search')),('job_position_applicant','ilike',kw.get('search'))])
            search_product = kw.get('search')
            resident_in_qatar = ''
        if kw.get('resident_in_qatar'):
            applicant_ids = request.env['job.vacancies.applicant'].sudo().search([('resident_in_qatar','=',kw.get('resident_in_qatar'))])
            resident_in_qatar = kw.get('resident_in_qatar')
            search_product = ''
        if kw.get('search') and kw.get('resident_in_qatar'):
            applicant_ids = request.env['job.vacancies.applicant'].sudo().search([('resident_in_qatar','=',kw.get('resident_in_qatar')),'|','|','|',('resume','ilike',kw.get('search')) , ('skills','ilike',kw.get('search')),('degree_applicant','ilike',kw.get('search')),('job_position_applicant','ilike',kw.get('search'))])
            print("........applicant_ids........",applicant_ids)
            search_product = kw.get('search')
            resident_in_qatar = kw.get('resident_in_qatar')
        return http.request.render('ebs_qsheild_mod.job_vacancies_job_seekeres_template',{'applicant_ids':applicant_ids,'search_product':search_product,'resident_in_qatar':resident_in_qatar})


    @http.route('/vacancies/applicant/seekers/record/', type='json', auth='public', website='True')
    def seekers_applicant_save(self, **kw):
        print(".......kw......",kw)
        applicant_id = request.env['job.vacancies.applicant'].sudo().browse(int(kw.get('seekers_job_vacancies_applicant_rec_id')))
        if kw.get('seekers_job_vacancies_applicant_rec_id'):
            company_id = request.env['job.vacancies.company'].sudo().search([('user_id', '=', request.env.user.id)],limit=1)
            if not company_id:
                company_id = request.env['job.vacancies.company'].sudo().create({
                    'name': request.env.user.partner_id.name,
                    'user_id': request.env.user.id
                })
            job_vac_sort_list_rec_id = request.env['application.company.sortlisting'].sudo().search([('applicant_name','=',int(kw.get('seekers_job_vacancies_applicant_rec_id'))),('company_name','=',company_id.id)])
            print("....job_vac_sort_list_rec_id..........",job_vac_sort_list_rec_id)

            if not job_vac_sort_list_rec_id:
                request.env['application.company.sortlisting'].sudo().create({
                    'company_position': applicant_id.job_position_applicant,
                    'company_name':company_id.id,
                    'applicant_name':applicant_id.id,
                })
                return True
        return False

    @http.route('/saved/application/company/', type='http', auth='public', website='True')
    def saved_application_company(self, **kw):
        print(".......kw......", kw)
        saved_sortlisted_seekers = request.env['application.company.sortlisting'].sudo().search([('company_name.user_id','=',request.env.user.id)])
        return http.request.render('ebs_qsheild_mod.save_sortlisted_applicant_tmp',
                                   {'saved_sortlisted_seekers':saved_sortlisted_seekers})



    @http.route('/search/vacancies/record', type='json', auth='public', website='True')
    def search_vacancies_rec(self, **kw):
            if kw.get('search_input'):
                vacancies_ids = request.env['job.vacancies'].sudo().search(['|','|',('position','ilike',kw.get('search_input')) , ('description','ilike',kw.get('search_input')),('skills_requirement','ilike',kw.get('search_input'))])
                return kw.get('search_input')


    @http.route('/search/jobseekers/record', type='json', auth='public', website='True')
    def search_jobseekers_rec(self, **kw):
        vals = {}
        print("............kw.............",kw)
        if kw.get('search_input'):
            vals.update({
                'search': kw.get('search_input'),
            })
        if kw.get('search_input_resident'):
            vals.update({
                'resident_in_qatar': kw.get('resident_in_qatar'),
            })
        if kw.get('search_input') and kw.get('search_input_resident'):
            vals.update({
                'search': kw.get('search_input'),
                'resident_in_qatar': kw.get('search_input_resident'),
            })

        return vals

    @http.route('/search/jobseekers/resident/record', type='json', auth='public', website='True')
    def search_jobseekers_resident_rec(self, **kw):
        vals = {}
        if kw.get('search_input'):
            vals.update({
                'search': kw.get('search_input'),
            })
        if kw.get('search_input_resident'):
            vals.update({
                'resident_in_qatar': kw.get('search_input_resident'),
            })
        if kw.get('search_input') and kw.get('search_input_resident'):
            vals.update({
                'search': kw.get('search_input'),
                'resident_in_qatar': kw.get('search_input_resident'),
            })
        print(".................vals.........",vals)
        return vals



    @http.route('/company/profile/info/', type='http', auth='public', website='True')
    def _company_profile_info_save(self, **kw):
        if kw.get('company_name'):
            request.env['job.vacancies.company'].sudo().create({
                'name': kw.get('company_name') if kw.get('company_name') else '',
                'industry_id': int(kw.get('job_company_industry') if kw.get('job_company_industry') else False),
                'number_of_employees': (kw.get('job_number_of_employees') if kw.get('job_number_of_employees') else '1-50'),
                'user_id': request.env.user.id,
            })
            return request.redirect('/job/company/account/')


    @http.route('/education/line/remove/', type='json', auth='public', website='True')
    def remove_education_info_line(self, **kw):
        if kw.get('education_info_line_id'):
            request.env['education.info'].sudo().browse(int(kw.get('education_info_line_id'))).unlink()
            return True


    @http.route('/point/of/contact/line/remove/', type='json', auth='public', website='True')
    def remove_point_of_contact_line(self, **kw):
        if kw.get('point_of_remove_line'):
            request.env['res.partner'].sudo().browse(int(kw.get('point_of_remove_line'))).unlink()
            return True

    @http.route('/job/history/line/remove/', type='json', auth='public', website='True')
    def remove_job_history_line(self, **kw):
        if kw.get('job_history_line_id'):
            request.env['job.history'].sudo().browse(int(kw.get('job_history_line_id'))).unlink()
            return True


class ContactsList(http.Controller):

    @http.route('/individual_contacts', type='http', auth='public', website='True')
    def get_individual_contacts(self, **post):
        individual_contact_domain = [('display_on_portal', '=', True), ('company_type', '=', 'person'),
                                     ('first_Nationality', '=', 'leb'), ('status', '!=', 'draft')]

        search_contacts = ''
        if post.get('search'):
            individual_contact_domain += ['|', ('name', 'ilike', post.get('search')),
                                          ('function', 'ilike', post.get('search'))]
            search_contacts = post.get('search')

        individual_contact_ids = request.env['res.partner'].sudo().search(individual_contact_domain)
        individual_contact_ids = individual_contact_ids.filtered(lambda o: o.company_type == 'person')

        values = {
            'individual_contact_ids': individual_contact_ids,
            'search_contacts': search_contacts
        }
        return http.request.render('ebs_qsheild_mod.individual_contacts_template', values)

    @http.route('/search/individual_contacts', type='json', auth='public', website='True')
    def search_individual_contacts(self, **kw):
        if kw.get('search_input'):
            return kw.get('search_input')

    @http.route('/company_contacts', type='http', auth='public', website='True')
    def get_company_contacts(self, **post):
        company_contact_domain = [('display_on_portal', '=', True), ('company_type', '=', 'company'),
                                  ('first_Nationality', '=', 'leb'), ('status', '!=', 'draft')]

        search_contacts = ''
        if post.get('search'):
            company_contact_domain += ['|', ('name', 'ilike', post.get('search')),
                                       ('industry_id.name', 'ilike', post.get('search'))]
            search_contacts = post.get('search')

        company_contact_ids = request.env['res.partner'].sudo().search(company_contact_domain)
        company_contact_ids = company_contact_ids.filtered(lambda o: o.company_type == 'company')

        values = {
            'company_contact_ids': company_contact_ids,
            'search_contacts': search_contacts
        }
        return http.request.render('ebs_qsheild_mod.company_contacts_template', values)

    @http.route('/search/company_contacts', type='json', auth='public', website='True')
    def search_company_contacts(self, **kw):
        if kw.get('search_input'):
            return kw.get('search_input')

    @http.route('/addresses/<int:contact_id>', type='http', auth='public', website='True')
    def get_addresses(self, contact_id, **post):
        contact_ids = request.env['res.partner'].sudo().browse(contact_id)
        addresses_ids = contact_ids.address_ids

        values = {
            'addresses_ids': addresses_ids,
            'company_type': contact_ids.company_type,
        }
        return http.request.render('ebs_qsheild_mod.company_addresses_template', values)

    @http.route('/social_media/<int:contact_id>', type='http', auth='public', website='True')
    def get_social_media(self, contact_id, **post):
        contact_ids = request.env['res.partner'].sudo().browse(contact_id)
        social_media_ids = contact_ids.social_media_ids

        values = {
            'social_media_ids': social_media_ids,
            'company_type': contact_ids.company_type,
        }
        return http.request.render('ebs_qsheild_mod.social_media_template', values)
