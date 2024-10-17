from builtins import print
from threading import local

from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError
from odoo.http import request
from odoo.tools.translate import _

from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.osv.expression import OR
from datetime import datetime, date
import binascii
import hmac
import hashlib
import json
import re
import json
import uuid
import array
import base64
from odoo.http import content_disposition, Controller, request, route

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT



class ContactPortal(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_home_portal_values()
        # if request.env.user.partner_id.status in ['draft','progress','reject'] and request.env.user.partner_id.person_type == 'emp':
        #     return request.render("ebs_qsheild_mod.description")
        # else:
        if request.env.user.partner_id.applicant_user_boolean:
            return request.redirect("/")
        else:
            return request.render("portal.portal_my_home", values)
        # return request.redirect("/")

    def _prepare_portal_layout_values(self):
        values = super(ContactPortal, self)._prepare_portal_layout_values()
        values['kadaa'] = request.env['ebs_mod.country.kaza'].sudo().search([])
        values['religion'] = request.env['ebs_mod.contact.religion'].sudo().search([])

        values['service_count'] = request.env['ebs_mod.service.types'].sudo().search_count(
            [('parent_service_id', '!=', False)])
        values['documentTypes'] = request.env['ebs_mod.document.types'].sudo().search([])
        values['region'] = request.env['ebs_mod.country.region'].sudo().search([])
        values['industries'] = request.env['res.partner.industry'].sudo().search([])
        values['job_ids'] = request.env['hr.job'].sudo().search([])
        values['social_media_types'] = request.env['ebs.socialmedia.types'].sudo().search([])

        serviceTypes = None
        user = request.env.user
        isLebanese = False
        isPalestinian = False
        isOthers = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
            serviceTypes = request.env['ebs_mod.service.types'].sudo().search([
                ('parent_service_id', '=', False)
                , ('for_lebanese', '=', isLebanese)
            ])
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
                serviceTypes = request.env['ebs_mod.service.types'].sudo().search([
                    ('parent_service_id', '=', False)
                    , ('for_palestinian', '=', isPalestinian)
                ])
            else:
                if user.partner_id.first_Nationality == 'other':
                    isOthers = True
                    serviceTypes = request.env['ebs_mod.service.types'].sudo().search([
                        ('parent_service_id', '=', False)
                        , ('for_others', '=', isOthers)
                    ])
        values['partner'] = user.partner_id

        values['notifications'] = request.env['ebs_mod.service.request.notification'].sudo().search([
            ('partner_id', '=', user.partner_id.id)
            , ('is_read', '=', False)
        ])

        values['serviceTypes'] = serviceTypes

        if values.get('sales_user', False):
            values['title'] = _("Salesperson")
        return values

    # Passport
    @http.route(['/my/passports', '/my/passports/page/<int:page>'], type='http', auth="public", website=True)
    def my_contact_passports(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                             search_in='content',
                             **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'date asc'},
        }
        searchbar_inputs = {
            'status': {'input': 'status', 'label': _('Status')},
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        s_domain = []
        if search and search_in:
            search_domain = []
            if search_in == 'status':
                search_domain = OR([search_domain, [('status', 'ilike', search)]])
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            s_domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].search_count(domain)
        pager = portal_pager(
            url="/my/passports",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        passports = request.env['ebs_mod.service.types'].sudo().search([('path', '=', '/passports')]
                                                                , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        passports_services = request.env['ebs_mod.service.types'].sudo().search(
            [('parent_service_id', '=', int(passports.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)

        child_service = [serv.id for serv in list(passports_services)]

        s_domain.append(('partner_id', '=', user.partner_id.id))
        s_domain.append(('service_type_id', 'in', child_service))
        service_request = request.env['ebs_mod.service.request'].sudo().search(s_domain, offset=pager['offset'], order=order)

        request.session['my_passports_history'] = passports.ids[:100]
        values.update({
            'date': date_begin,
            'passports': passports,
            'passports_services': passports_services,
            'service_request': service_request,
            'page_name': 'passports',
            'default_url': '/my/passports',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        if not request.env.user.has_group('base.group_public'):
            return request.render("ebs_qsheild_mod.portal_contact_passports", values)
        else:
            passports_services = request.env['ebs_mod.service.types'].sudo().search(
                [('parent_service_id', '=', int(passports.id)), '|'
                    , ('for_lebanese', '=', True)
                    , ('for_palestinian', '=', True)]
                )
            return request.render("ebs_qsheild_mod.portal_logout_contact_passports", {'passports_services':passports_services})

    @http.route(['/my/passports/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_passports_insert_doc_form(self, id=None):
        user = request.env.user
        print("-------------kw------------------", self)
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open Request."))
        documentTypes = request.env['ebs_mod.document.types'].sudo().search([])

        documents = service_request.document_in
        values = {
            'page_name': 'passports_insert',
            'service_request': service_request,
            'documents': documents,
            'partner': user.partner_id,
            'documentTypes': documentTypes,
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([])
        }

        return request.render("ebs_qsheild_mod.portal_contact_passports_form", values)

    @http.route(['/my/passports/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_passports_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None
        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].sudo().search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            document_type = document.document_type_id
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].sudo().create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        values = {
            'page_name': 'passports_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }

        return request.render("ebs_qsheild_mod.portal_contact_passports_form", values)

    # Personal Info
    @http.route(['/my/personal', '/my/personal/page/<int:page>'], type='http', auth="public", website=True)
    def my_contact_personal(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                            search_in='content',
                            **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'create_date asc'},
        }
        searchbar_inputs = {
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        # pager
        pager = portal_pager(
            url="/my/personal",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=0,
            page=page,
            step=self._items_per_page
        )

        personal = request.env['ebs_mod.service.types'].sudo().search([('path', '=', '/personal')]
                                                               , order=order, limit=1
                                                               , offset=pager['offset'])
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        personal_services = request.env['ebs_mod.service.types'].sudo().search(
            [('parent_service_id', '=', int(personal.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , order=order, limit=self._items_per_page
            , offset=pager['offset'])

        child_service = [serv.id for serv in list(personal_services)]

        service_request = request.env['ebs_mod.service.request'].sudo().search([('partner_id', '=', user.partner_id.id),
                                                                         ('service_type_id', 'in',
                                                                          child_service)])
        request.session['my_personal_history'] = personal.ids[:100]

        values.update({
            'date': date_begin,
            'personal': personal,
            'personal_services': personal_services,
            'service_request': service_request,
            'partner': user.partner_id,
            'page_name': 'personal',
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
            'default_url': '/my/personal',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })

        if not request.env.user.has_group('base.group_public'):
            return request.render("ebs_qsheild_mod.portal_contact_personal", values)
        else:
            personal_services = request.env['ebs_mod.service.types'].sudo().search(
                [('parent_service_id', '=', int(personal.id)), '|'
                    , ('for_lebanese', '=', True)
                    , ('for_palestinian', '=', True)]
                , order=order, limit=self._items_per_page
                , offset=pager['offset'])
            return request.render("ebs_qsheild_mod.portal_logout_contact_passports",
                                  {'passports_services': personal_services})

    @http.route(['/my/personal/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_personal_insert_doc_form(self, id):
        user = request.env.user
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open Request."))
        documentTypes = request.env['ebs_mod.document.types'].sudo().search([])
        documents = service_request.document_in

        values = {
            'page_name': 'personal_insert',
            'service_request': service_request,
            'documents': documents,
            'partner': user.partner_id,
            'documentTypes': documentTypes,
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([])
        }

        return request.render("ebs_qsheild_mod.portal_contact_personal_form", values)

    @http.route(['/my/personal/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_personal_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None
        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].sudo().search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None, })
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None, })
            document_type = document.document_type_id
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].sudo().create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        # personal_insert
        values = {
            'page_name': 'personal_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }

        return request.render("ebs_qsheild_mod.portal_contact_personal_form", values)

    # Visa
    @http.route(['/my/ta2shirat', '/my/ta2shirat/page/<int:page>'], type='http', auth="public", website=True)
    def my_contact_visa(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                        search_in='content',
                        **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'date asc'},
        }
        searchbar_inputs = {
            'status': {'input': 'status', 'label': _('Status')},
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        s_domain = []
        if search and search_in:
            search_domain = []
            if search_in == 'status':
                search_domain = OR([search_domain, [('status', 'ilike', search)]])
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            s_domain += search_domain

        # pager
        pager = portal_pager(
            url="/my/authorization",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=0,
            page=page,
            step=self._items_per_page
        )

        visa = request.env['ebs_mod.service.types'].sudo().search([('path', '=', '/ta2shirat')]
                                                           , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        visa_services = request.env['ebs_mod.service.types'].sudo().search(
            [('parent_service_id', '=', int(visa.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)

        child_service = [serv.id for serv in list(visa_services)]

        s_domain.append(('partner_id', '=', user.partner_id.id))
        s_domain.append(('service_type_id', 'in', child_service))
        service_request = request.env['ebs_mod.service.request'].sudo().search(s_domain, offset=pager['offset'], order=order)

        request.session['my_visa_history'] = visa.ids[:100]
        values.update({
            'date': date_begin,
            'visa': visa,
            'visa_services': visa_services,
            'service_request': service_request,
            'page_name': 'visa',
            'default_url': '/my/ta2shirat',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })

        if not request.env.user.has_group('base.group_public'):
            return request.render("ebs_qsheild_mod.portal_contact_visa", values)
        else:
            visa_services = request.env['ebs_mod.service.types'].sudo().search(
                [('parent_service_id', '=', int(visa.id)), '|'
                    , ('for_lebanese', '=', True)
                    , ('for_palestinian', '=', True)]
                , limit=self._items_per_page)
            return request.render("ebs_qsheild_mod.portal_logout_contact_passports",
                                  {'passports_services': visa_services})

    @http.route(['/my/ta2shirat/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_ta2shirat_insert_doc_form(self, id):
        user = request.env.user
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open Request."))
        documentTypes = request.env['ebs_mod.document.types'].sudo().search([])
        documents = service_request.document_in

        values = {
            'page_name': 'visa_insert',
            'service_request': service_request,
            'documents': documents,
            'documentTypes': documentTypes
        }

        return request.render("ebs_qsheild_mod.portal_contact_visa_form", values)

    @http.route(['/my/ta2shirat/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_ta2shirat_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None
        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].sudo().search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            document_type = document.document_type_id
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].sudo().create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        # ta2shirat_insert
        values = {
            'page_name': 'ta2shirat_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }
        return request.render("ebs_qsheild_mod.portal_contact_visa_form", values)

    @http.route(['/create_personal_service_request'], type='http', auth="user", website=True)
    def create_personal_service_request(self, **kw):
        user = request.env.user
        authorization = request.env['ebs_mod.service.types'].search([('path', '=', '/personal')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        personal_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)
        values = {
            'personal_services': personal_services,
            'page_name': 'newservice',
        }
        return request.render('ebs_qsheild_mod.create_personal_service_request', values)

    @http.route(['/create_visa_service_request'], type='http', auth="user", website=True)
    def create_visa_service_request(self, **kw):
        user = request.env.user
        authorization = request.env['ebs_mod.service.types'].search([('path', '=', '/ta2shirat')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        visa_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)
        values = {
            'visa_services': visa_services,
            'page_name': 'newservice',
        }
        return request.render('ebs_qsheild_mod.create_visa_service_request', values)

    @http.route(['/create_tasdikat_service_request'], type='http', auth="user", website=True)
    def create_tasdikat_service_request(self, **kw):
        user = request.env.user
        authorization = request.env['ebs_mod.service.types'].search([('path', '=', '/tasdkiat')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        tasdkiat_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)
        values = {
            'tasdikat_services': tasdkiat_services,
            'page_name': 'newservice',
        }
        return request.render('ebs_qsheild_mod.create_tasdikat_service_request', values)

    @http.route(['/create_ifadat_service_request'], type='http', auth="user", website=True)
    def create_tasdikat_service_request(self, **kw):
        user = request.env.user
        authorization = request.env['ebs_mod.service.types'].search([('path', '=', '/ifadat')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        ifadat_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)
        values = {
            'ifadat_services': ifadat_services,
            'page_name': 'newservice',
        }
        return request.render('ebs_qsheild_mod.create_ifadat_service_request', values)

    @http.route(['/create_service_request'], type='http', auth="user", website=True)
    def create_service_request(self, **kw):
        user = request.env.user
        authorization = request.env['ebs_mod.service.types'].search([('path', '=', '/authorization')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        authorization_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)
        values = {
            'authorization_services': authorization_services,
            'page_name': 'newservice',
        }
        return request.render('ebs_qsheild_mod.create_service_request', values)

    @http.route(['/my/authorization', '/my/authorization/page/<int:page>'], type='http', auth="public", website=True)
    def my_contact_authorization(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                                 search_in='content',
                                 **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'date asc'},
        }
        searchbar_inputs = {
            'status': {'input': 'status', 'label': _('Status')},
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        s_domain = []
        if search and search_in:
            search_domain = []
            if search_in == 'status':
                search_domain = OR([search_domain, [('status', 'ilike', search)]])
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            s_domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/authorization",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        authorization = request.env['ebs_mod.service.types'].sudo().search([('path', '=', '/authorization')]
                                                                    , limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        authorization_services = request.env['ebs_mod.service.types'].sudo().search(
            [('parent_service_id', '=', int(authorization.id)), '|'
                , ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)

        child_service = [serv.id for serv in list(authorization_services)]

        s_domain.append(('partner_id', '=', user.partner_id.id))
        s_domain.append(('service_type_id', 'in', child_service))
        service_request = request.env['ebs_mod.service.request'].sudo().search(s_domain, offset=pager['offset'], order=order)
        request.session['my_authorization_history'] = authorization.ids[:100]
        values.update({
            'date': date_begin,
            'authorization': authorization,
            'authorization_services': authorization_services,
            'service_request': service_request,
            'page_name': 'authorization',
            'default_url': '/my/authorization',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })

        if not request.env.user.has_group('base.group_public'):
            return request.render("ebs_qsheild_mod.portal_contact_authorization", values)
        else:
            authorization_services = request.env['ebs_mod.service.types'].sudo().search(
                [('parent_service_id', '=', int(authorization.id)), '|'
                    , ('for_lebanese', '=', True)
                    , ('for_palestinian', '=', True)]
                , limit=self._items_per_page)
            return request.render("ebs_qsheild_mod.portal_logout_contact_passports",
                                  {'passports_services': authorization_services})

    @http.route(['/my/services/delete', '/my/services/delete/<int:id>'], type='http', auth='user', website=True)
    def services_delete(self, id=None, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        if not id:
            service_id = request.params['service_id']
        else:
            service_id = id
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', partner.id)])

        service.sudo().unlink()

        return request.make_response(json.dumps({
            'status': "success",
            'data': {}
        }), headers=headers)

    @http.route(['/my/services/hideNotification/<int:id>'], type='http', auth='user', website=True)
    def hide_notification(self, id, **post):
        headers = [('Content-Type', 'application/json')]

        partner = request.env.user.partner_id

        notification = request.env['ebs_mod.service.request.notification'].search(
            [('id', '=', id), ('partner_id', '=', partner.id)])

        notification.sudo().write({'is_read': True})
        return request.make_response(json.dumps({
            'status': "success",
            'data': {}
        }), headers=headers)

    @http.route(['/my/service/change_doc'], type='http', auth='user', website=True)
    def change_documents(self, **post):
        print(".......change_documents***********post***.....",post)
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        service_id = request.params['service_id']
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', partner.id)])

        if post.__contains__('beneficiary'):
            beneficiary = request.params['beneficiary']
            service_request.sudo().write({'service_beneficiary': beneficiary})

        service_request.sudo().write({'document_in': None})
        beneficiary_partner = request.env['res.partner'].search([('id', '=', beneficiary)])
        folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
        partner_documents = request.env['documents.document'].sudo().search(
            [('partner_id', '=', beneficiary_partner.id)])

        list_partner_docs = [doc.document_type_id.id for doc in list(partner_documents)]

        if beneficiary_partner.id == partner.id:
            document_owner = 'me'
        else:
            document_owner = 'family'
        for docs in list(service_request.service_type_id.document_types):
            if docs.id in list_partner_docs:
                documents = request.env['documents.document'].sudo().search(
                    [('partner_id', '=', service_request.service_beneficiary.id),
                     ('document_type_id', '=', docs.id)], limit=1)
                service_request.sudo().write({'document_in': [(4, documents.id)]})
            else:
                documents = request.env['documents.document'].sudo().create({
                    'partner_id': service_request.service_beneficiary.id,
                    'type': 'binary',
                    'document_owner': document_owner,
                    'document_type_id': docs.id,
                    'folder_id': folder.id
                })
                service_request.sudo().write({'document_in': [(4, documents.id)]})
        if post.get('beneficiary'):
            beneficiary = request.env['res.partner'].sudo().search([('id','=',int(post.get('beneficiary')))])
            beneficiary_qid_obj = request.env['ebs_mod.contact.ikama'].sudo().search([('partner_id', '=', beneficiary.id), ('is_active', '=', True),
                 ('family_member', '=', 'spouse')], limit=1, order='id desc')
            beneficiary_lebnon = request.env['ebs_mod.contact.address'].sudo().search([('partner_id','=',beneficiary.id),('is_active','=',True),('type','=','Lebanon')],limit=1,order='id desc')
            beneficiary_qatar = request.env['ebs_mod.contact.address'].sudo().search([('partner_id','=',beneficiary.id),('is_active','=',True),('type','=','Qatar')],limit=1,order='id desc')
            # all_spouse_data = {rec.id: rec.name for rec in all_beneficiary}
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'beneficiary_archive_no': beneficiary.archive_number,
                     'beneficiary_name': beneficiary.firstName +' '+ beneficiary.middleName +' '+ beneficiary.lastName,
                     'beneficiary_nationality': beneficiary.first_Nationality,
                     'beneficiary_qid': beneficiary_qid_obj.ikama_no,
                     'beneficiary_spose_name': beneficiary_qid_obj.dependent.name,
                     'beneficiary_nationality_spouse': beneficiary_qid_obj.dependent.first_Nationality,
                     'beneficiary_sponsor': beneficiary.company_id.name,
                     'beneficiary_sponsor_mobile': beneficiary.company_id.phone,
                     'beneficiary_lebnon_street': beneficiary_lebnon.street,
                     'beneficiary_lebnon_owned': beneficiary_lebnon.owned,
                     'beneficiary_lebnon_floor': beneficiary_lebnon.floor,
                     'beneficiary_lebnon_mobile':  beneficiary_lebnon.mobile,
                     'beneficiary_qatar_street': beneficiary_qatar.street,
                     'beneficiary_qatar_building': beneficiary_qatar.building,
                     'beneficiary_qatar_floor':  beneficiary_qatar.floor,
                     'beneficiary_qatar_mobile': beneficiary_qatar.mobile,
                     'beneficiary':beneficiary.id,
                     'beneficiary_qid_obj':beneficiary_qid_obj.dependent.id,

                     }
        }), headers=headers)

    @http.route(['/my/authorization/submit_authorization'], type='http', auth='user', website=True)
    def contact_submit_auth(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        service_id = request.params['service_id']
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', partner.id)])

        description = request.params['description']
        account_number = ''
        bank_name = ''
        branch = ''
        agent_address = ''
        if post.__contains__('beneficiary'):
            beneficiary = request.params['beneficiary']
            service.sudo().write({'service_beneficiary': beneficiary})

        if post.__contains__('agent_address'):
            agent_address = request.params['agent_address']
        if post.__contains__('account_number'):
            account_number = request.params['account_number']
        if post.__contains__('bank_name'):
            bank_name = request.params['bank_name']
        if post.__contains__('branch'):
            branch = request.params['branch']
        # PASSPORTS
        if service.service_type_id.code in '01-06':
            if post.__contains__('consular_number'):
                consular_number = request.params['consular_number']
            if post.__contains__('receipt_number'):
                receipt_number = request.params['receipt_number']
            release_Date = None
            if post.__contains__('release_Date'):
                release_Date = request.params['release_Date']

            service.sudo().write({'consular_number': consular_number,
                                  'receipt_number': receipt_number,
                                  'release_Date': datetime.strptime(release_Date, '%d/%m/%Y') if release_Date else None,
                                  })

        if service.service_type_id.code in '04-05':
            renewal_nb = None
            if post.__contains__('renewal_nb'):
                renewal_nb = request.params['renewal_nb']
            renewal_date = None
            if post.__contains__('renewal_date'):
                renewal_date = request.params['renewal_date']
            renewal_passport_period = None
            if post.__contains__('renewal_passport_period'):
                renewal_passport_period = request.params['renewal_passport_period']
            renewal_receipt_number = None
            if post.__contains__('renewal_receipt_number'):
                renewal_receipt_number = request.params['renewal_receipt_number']
            # renewal_date =
            service.sudo().write({'renewal_nb': renewal_nb,
                                  'renewal_date': datetime.strptime(renewal_date, '%d/%m/%Y') if renewal_date else None,
                                  'passport_period': renewal_passport_period,
                                  'receipt_number': renewal_receipt_number
                                  })
            print("==================952--------------", renewal_date)

        if service.service_type_id.code in ('01-01', '01-02'):
            passport_period = None
            if post.__contains__('passport_period'):
                passport_period = request.params['passport_period']

            current_passport_type = None
            if post.__contains__('current_passport_type'):
                current_passport_type = request.params['current_passport_type']
            with_husband_name = False
            if post.__contains__('with_husband_name'):
                if request.params['with_husband_name'] == 'on':
                    with_husband_name = True
            dhl25 = False
            if post.__contains__('dhl25'):
                if request.params['dhl25'] == 'on':
                    dhl25 = True
            pal_doc_period = None
            if post.__contains__('pal_doc_period'):
                pal_doc_period = request.params['pal_doc_period']
            if post.__contains__('current_passport_type_pal'):
                current_passport_type = request.params['current_passport_type_pal']

            received_by = None
            if post.__contains__('received_by'):
                received_by = request.params['received_by']

            dhl30 = False
            if post.__contains__('dhl30'):
                if request.params['dhl30'] == 'on':
                    dhl30 = True
            documentNo = None
            if post.__contains__('documentNo'):
                documentNo = request.params['documentNo']
            release_Date = None
            if post.__contains__('release_Date'):
                release_Date = request.params['release_Date']

            service.sudo().write({'passport_period': passport_period,
                                  'with_husband_name': with_husband_name,
                                  'current_passport_type': current_passport_type,
                                  'dhl25': dhl25,
                                  'release_Date': datetime.strptime(release_Date, '%d/%m/%Y') if release_Date else None,
                                  'pal_doc_period': pal_doc_period,
                                  'received_by': received_by,
                                  'dhl30': dhl30,
                                  'documentNo': documentNo
                                  })

        # VISA
        if service.service_type_id.code in '04-02':
            if post.__contains__('purpose_of_trip'):
                purpose_of_trip = request.params['purpose_of_trip']
            if post.__contains__('visa_duration'):
                visa_duration = request.params['visa_duration']
            if post.__contains__('nb_entries'):
                nb_entries = request.params['nb_entries']
            if post.__contains__('entry_point'):
                entry_point = request.params['entry_point']
            if post.__contains__('expected_arrival_day'):
                expected_arrival_day = request.params['expected_arrival_day']
            if post.__contains__('expected_departure_day'):
                expected_departure_day = request.params['expected_departure_day']
            if post.__contains__('visa_no'):
                visa_no = request.params['visa_no']
            if post.__contains__('receipt_no'):
                receipt_no = request.params['receipt_no']

            service.sudo().write({'purpose_of_trip': purpose_of_trip,
                                  'visa_duration': visa_duration,
                                  'nb_entries': nb_entries,
                                  'entry_point': entry_point,
                                  'expected_arrival_day': datetime.strptime(expected_arrival_day,
                                                                            '%d/%m/%Y') if expected_arrival_day else None,
                                  'expected_departure_day': datetime.strptime(expected_departure_day,
                                                                              '%d/%m/%Y') if expected_departure_day else None,
                                  'visa_no': visa_no,
                                  'receipt_no': receipt_no})

        # Personal
        if service.service_type_id.code in ('02-02', '02-04'):
            if post.__contains__('spouse'):
                spouse = request.params['spouse']
                dependent = request.env['res.partner'].search(
                    ['&', ('id', '=', spouse), ('parent_id', '=', partner.id)])
                passport = request.env['ebs_mod.contact.passport'].search(
                    ['&', ('dependent', '=', dependent.id), ('is_active', '=', True)])
                ikama = request.env['ebs_mod.contact.ikama'].search(
                    ['&', ('dependent', '=', dependent.id), ('is_active', '=', True)])

                service.sudo().write({'spouse': dependent.id,
                                      'spouse_passport': passport.id,
                                      'spouse_ikama': ikama.id})

        if service.service_type_id.code == '02-04':
            if post.__contains__('childfirstName'):
                childfirstName = request.params['childfirstName']
            if post.__contains__('childmiddleName'):
                childmiddleName = request.params['childmiddleName']
            if post.__contains__('childlastName'):
                childlastName = request.params['childlastName']
            if post.__contains__('childfirstName_EN'):
                childfirstName_EN = request.params['childfirstName_EN']
            if post.__contains__('childmiddleName_EN'):
                childmiddleName_EN = request.params['childmiddleName_EN']
            if post.__contains__('childlastName_EN'):
                childlastName_EN = request.params['childlastName_EN']
            if post.__contains__('childdate'):
                childdate = request.params['childdate']
            if post.__contains__('childplaceOfBirth'):
                childplaceOfBirth = request.params['childplaceOfBirth']
            if post.__contains__('child_gender'):
                child_gender = request.params['child_gender']
            child_birth_certificate_date = None
            child_birth_certificate = None
            if post.__contains__('child_birth_certificate_date'):
                child_birth_certificate_date = request.params['child_birth_certificate_date']
            if child_birth_certificate_date == '':
                child_birth_certificate_date = None
            if post.__contains__('child_birth_certificate'):
                child_birth_certificate = request.params['child_birth_certificate']

            if post.__contains__('child_birth_registration'):
                child_birth_registration = request.params['child_birth_registration']
            if post.__contains__('child_birth_registration_date'):
                child_birth_registration_date = request.params['child_birth_registration_date']
            if post.__contains__('birth_registry_number'):
                birth_registry_number = request.params['birth_registry_number']
            if post.__contains__('birth_record_page'):
                birth_record_page = request.params['birth_record_page']
            if post.__contains__('record_personal_status'):
                record_personal_status = request.params['record_personal_status']
            if post.__contains__('record_transaction_number'):
                record_transaction_number = request.params['record_transaction_number']
            if post.__contains__('starting_date'):
                starting_date = request.params['starting_date']
            if post.__contains__('child_passport_number'):
                child_passport_number = request.params['child_passport_number']
            service.sudo().write({'child_birth_certificate_date': datetime.strptime(child_birth_certificate_date,
                                                                                    '%d/%m/%Y') if child_birth_certificate_date else None,
                                  'child_birth_certificate': child_birth_certificate,
                                  'child_birth_registration': child_birth_registration,
                                  'child_birth_registration_date': datetime.strptime(child_birth_registration_date,
                                                                                     '%d/%m/%Y') if child_birth_registration_date else None,
                                  'birth_registry_number': birth_registry_number,
                                  'birth_record_page': birth_record_page,
                                  'record_personal_status': record_personal_status,
                                  'record_transaction_number': record_transaction_number,
                                  'starting_date': datetime.strptime(starting_date,
                                                                     '%d/%m/%Y') if starting_date else None,
                                  'child_passport_number': child_passport_number})
            dependent_type = 'child'
            name = childfirstName + ' ' + childmiddleName + ' ' + childlastName
            dependent = service.child

            if not dependent:
                dependent = request.env['res.partner'].create({
                    'name': name,
                    'firstName': childfirstName,
                    'middleName': childmiddleName,
                    'lastName': childlastName,
                    'first_name_en': childfirstName_EN,
                    'middle_name_en': childmiddleName_EN,
                    'last_name_en': childlastName_EN,
                    'dependent_type': dependent_type,
                    'gender': child_gender,
                    'person_type': 'child',
                    'parent_id': partner.id,
                    'placeOfBirth': childplaceOfBirth,
                    'date': datetime.strptime(childdate, '%d/%m/%Y') if childdate else None,
                })

                service.sudo().write({'child': dependent})
            else:
                dependent.write({
                    'name': name,
                    'firstName': childfirstName,
                    'middleName': childmiddleName,
                    'lastName': childlastName,
                    'first_name_en': childfirstName_EN,
                    'middle_name_en': childmiddleName_EN,
                    'last_name_en': childlastName_EN,
                    'placeOfBirth': childplaceOfBirth,
                    'date': datetime.strptime(childdate, '%d/%m/%Y') if childdate else None,
                    'gender': child_gender,
                })

        if service.service_type_id.code in ('02-01', '02-03'):
            if post.__contains__('depfirstName'):
                depfirstName = request.params['depfirstName']
            if post.__contains__('depmiddleName'):
                depmiddleName = request.params['depmiddleName']
            if post.__contains__('deplastName'):
                deplastName = request.params['deplastName']
            if post.__contains__('depfirstName_EN'):
                depfirstName_EN = request.params['depfirstName_EN']
            if post.__contains__('depmiddleName_EN'):
                depmiddleName_EN = request.params['depmiddleName_EN']
            if post.__contains__('deplastName_EN'):
                deplastName_EN = request.params['deplastName_EN']
            if post.__contains__('depdate'):
                depdate = request.params['depdate']
            if post.__contains__('depplaceOfBirth'):
                depplaceOfBirth = request.params['depplaceOfBirth']
            if post.__contains__('depkazaBirth'):
                depkazaBirth = request.params['depkazaBirth']
            if post.__contains__('depsejelNo'):
                depsejelNo = request.params['depsejelNo']
            if post.__contains__('depnationality'):
                depnationality = request.params['depnationality']
            if depnationality == '':
                depnationality = None
            else:
                depnationality = int(depnationality)

            if post.__contains__('depsec_natio'):
                depsec_natio = request.params['depsec_natio']

            if depsec_natio == '':
                depsec_natio = None
            else:
                depsec_natio = int(depsec_natio)
            if post.__contains__('depreligion'):
                depreligion = request.params['depreligion']
            if post.__contains__('occupation'):
                occupation = request.params['occupation']
            if post.__contains__('depfather_fullname'):
                depfather_fullname = request.params['depfather_fullname']
            if post.__contains__('depmotherFullName'):
                depmotherFullName = request.params['depmotherFullName']
            dependent_type = 'spouse'
            name = depfirstName + ' ' + depmiddleName + ' ' + deplastName
            dependent = service.spouse

            if not dependent:
                dependent = request.env['res.partner'].create({
                    'name': name,
                    'firstName': depfirstName,
                    'middleName': depmiddleName,
                    'lastName': deplastName,
                    'first_name_en': depfirstName_EN,
                    'middle_name_en': depmiddleName_EN,
                    'last_name_en': deplastName_EN,
                    'dependent_type': dependent_type,
                    'person_type': 'child',
                    'parent_id': partner.id,
                    'nationality': depsec_natio,
                    'country_id': depnationality,
                    'sejelNo': depsejelNo,
                    'function': occupation,
                    'motherFullName': depmotherFullName,
                    'placeOfBirth': depplaceOfBirth,
                    'date': datetime.strptime(depdate, '%d/%m/%Y') if depdate else None,
                    'father_fullname': depfather_fullname,
                    'kazaBirth': depkazaBirth,
                    'religion': depreligion
                })
                service.sudo().write({'spouse': dependent})

            else:
                vals = {
                    'name': name,
                    'firstName': depfirstName,
                    'middleName': depmiddleName,
                    'lastName': deplastName,
                    'first_name_en': depfirstName_EN,
                    'middle_name_en': depmiddleName_EN,
                    'last_name_en': deplastName_EN,
                    'nationality': depsec_natio,
                    'country_id': depnationality,
                    'sejelNo': depsejelNo,
                    'function': occupation,
                    'motherFullName': depmotherFullName,
                    'placeOfBirth': depplaceOfBirth,
                    'date': datetime.strptime(depdate, '%d/%m/%Y') if depdate else None,
                    'father_fullname': depfather_fullname,
                    'kazaBirth': depkazaBirth,
                    'religion': depreligion
                }
                dependent.write(vals)

            if service.service_type_id.code in '02-03':
                if post.__contains__('depmarriage_date'):
                    depmarriage_date = request.params['depmarriage_date']
                if post.__contains__('depmarriage_place'):
                    depmarriage_place = request.params['depmarriage_place']

                dependent.sudo().write(
                    {'marriage_date': datetime.strptime(depmarriage_date, '%d/%m/%Y') if depmarriage_date else None,
                     'marriage_place': depmarriage_place})

            if post.__contains__('passport_no'):
                passport_no = request.params['passport_no']
            if post.__contains__('passport_place'):
                passport_place = request.params['passport_place']
            if post.__contains__('passport_start_date'):
                passport_start_date = request.params['passport_start_date']
            if passport_start_date == '':
                passport_start_date = None
            if post.__contains__('passport_exp_date'):
                passport_exp_date = request.params['passport_exp_date']
            if passport_exp_date == '':
                passport_exp_date = None

            passport = service.spouse_passport
            if not passport.id:
                vals = {
                    'passport_no': passport_no,
                    'passport_place': passport_place,
                    'passport_start_date': datetime.strptime(passport_start_date, '%d/%m/%Y'),
                    'passport_exp_date': datetime.strptime(passport_exp_date, '%d/%m/%Y'),
                    'is_active': True,
                    'partner_id': partner.id,
                    'family_member': 'spouse',
                    'dependent': dependent.id
                }
                passport = request.env['ebs_mod.contact.passport'].create(vals)
                service.sudo().write({'spouse_passport': passport.id})
            else:
                passport.write({
                    'passport_no': passport_no,
                    'passport_place': passport_place,
                    'passport_start_date': datetime.strptime(passport_start_date,
                                                             '%d/%m/%Y') if passport_start_date else None,
                    'passport_exp_date': datetime.strptime(passport_exp_date,
                                                           '%d/%m/%Y') if passport_exp_date else None,
                    'is_active': True
                })

            if post.__contains__('ikama_no'):
                ikama_no = request.params['ikama_no']
            if post.__contains__('ikama_enddate'):
                ikama_enddate = request.params['ikama_enddate']
            if post.__contains__('guarantor'):
                guarantor = request.params['guarantor']

            ikama = service.spouse_ikama
            if not ikama.id:
                ikama = request.env['ebs_mod.contact.ikama'].create({
                    'ikama_enddate': datetime.strptime(ikama_enddate, '%d/%m/%Y') if ikama_enddate else None,
                    'ikama_no': ikama_no,
                    'dependent': dependent.id,
                    'guarantor': guarantor,
                    'occupation': occupation,
                    'is_active': True,
                    'partner_id': partner.id,
                    'family_member': 'spouse'
                })
                service.sudo().write({'spouse_ikama': ikama.id})
            else:
                ikama.write({
                    'ikama_enddate': datetime.strptime(ikama_enddate, '%d/%m/%Y') if ikama_enddate else None,
                    'ikama_no': ikama_no,
                    'guarantor': guarantor,
                    'occupation': occupation,
                    'is_active': True
                })

        if service.code:
            code = service.code
        else:
            code = service.env['ir.sequence'].next_by_code('ebs_mod.service.request')

        year = str(service.date.year)
        month = service.date.strftime("%B")
        service_red = service.service_type_id.code or ""

        name = service_red + "-" + month + year + "-" + code
        status = 'progress'
        service.sudo().write({'status': status,
                              'code': code,
                              'name': name,
                              'desc': description,
                              'account_number': account_number,
                              'bank_name': bank_name,
                              'branch': branch,
                              'agent_address': agent_address
                              })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': service.id}
        }), headers=headers)

    @http.route(['/my/authorization/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_auth_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None

        document_owner = request.params['document_owner'] or None
        document_owner_name = request.params['document_owner_name'] or None
        document_owner_description = request.params['document_owner_description'] or None

        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].sudo().search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                                'document_owner': document_owner,
                                'document_owner_name': document_owner_name,
                                'document_owner_description': document_owner_description})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                                'document_owner': document_owner,
                                'document_owner_name': document_owner_name,
                                'document_owner_description': document_owner_description
                                })
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].sudo().create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
                'document_owner': document_owner,
                'document_owner_name': document_owner_name,
                'document_owner_description': document_owner_description
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        # authorization_insert
        values = {
            'page_name': 'authorization_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }

        return request.render("ebs_qsheild_mod.portal_contact_authorization_form", values)

    @http.route(['/my/authorization/document/open/<int:id>'], type='http', auth='user', website=True)
    def documents_auth_open(self, id, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        service_id = request.params['service_id']
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', partner.id)])
        description = ''
        if 'description' in request.params:
            description = request.params['description']
        account_number = ''
        bank_name = ''
        branch = ''
        agent_address = ''
        if post.__contains__('agent_address'):
            agent_address = request.params['agent_address']
        if post.__contains__('account_number'):
            account_number = request.params['account_number']
        if post.__contains__('bank_name'):
            bank_name = request.params['bank_name']
        if post.__contains__('branch'):
            branch = request.params['branch']

        service.sudo().write({'desc': description,
                              'account_number': account_number,
                              'bank_name': bank_name,
                              'branch': branch,
                              'agent_address': agent_address
                              })

        document = request.env['documents.document'].sudo().search([('id', '=', id)])
        doc = ""
        if document.document_number:
            doc = document.document_number

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'documentId': document.id,
                     'doctype': document.document_type_id.id,
                     'document_number': doc,
                     'name': document.name,
                     'is_required_issue_date': document.document_type_id.is_required_issue_date,
                     'is_required_expiry_date': document.document_type_id.is_required_expiry_date,
                     'is_required_doc_no': document.document_type_id.is_required_doc_no,
                     # 'issue_date': document.issue_date,
                     # 'expiry_date': document.expiry_date,
                     'service_id': service_id,
                     'document_owner': document.document_owner,
                     }
        }), headers=headers)

    @http.route(['/my/authorization/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_authorization_insert_doc_form(self, id):
        user = request.env.user
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open ."))
        else:
            documentTypes = request.env['ebs_mod.document.types'].sudo().search([])
            documents = service_request.document_in

            values = {
                'page_name': 'authorization_insert',
                'service_request': service_request,
                'documents': documents,
                'documentTypes': documentTypes
            }

            return request.render("ebs_qsheild_mod.portal_contact_authorization_form", values)

    @http.route(['/my/authorization/insert_form', '/my/authorization/insert_form/page/<int:page>'], type='http'
        , auth="user", website=True)
    def contact_authorization_insert_form(self, **post):
        headers = [('Content-Type', 'application/json')]
        user = request.env.user
        partner = user.partner_id
        print(request.params, "##################################")
        today = date.today()
        services = request.env['ebs_mod.service.types'].search(
            [('name', '=', request.params['service'])], limit=1)

        service_request = request.env['ebs_mod.service.request'].create({
            'partner_id': request.env.user.partner_id.id,
            'date': today,
            'service_type_id': services.id,
        })
        id = service_request.id

        folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
        partner_documents = request.env['documents.document'].sudo().search([('partner_id', '=', partner.id)])

        list_partner_docs = [doc.document_type_id.id for doc in list(partner_documents)]

        for docs in list(services.document_types):
            if docs.id in list_partner_docs:
                documents = request.env['documents.document'].sudo().search([('partner_id', '=', partner.id),
                                                                             ('document_type_id', '=', docs.id)],
                                                                            limit=1)
                service_request.sudo().write({'document_in': [(4, documents.id)]})
            else:
                documents = request.env['documents.document'].sudo().create({
                    'partner_id': partner.id,
                    'type': 'binary',
                    'document_type_id': docs.id,
                    'folder_id': folder.id
                })
                service_request.sudo().write({'document_in': [(4, documents.id)]})
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': id
                     }
        }), headers=headers)

    @http.route(['/my/service/insert_form', '/my/service/insert_form/page/<int:page>'], type='json'
        , auth="user", website=True)
    def contact_service_insert_form(self, **post):
        headers = [('Content-Type', 'application/json')]
        user = request.env.user
        partner = user.partner_id
        today = date.today()
        services = request.env['ebs_mod.service.types'].search(
            [('name', '=', request.params['service'])], limit=1)

        service_request = request.env['ebs_mod.service.request'].create({
            'partner_id': request.env.user.partner_id.id,
            'date': today,
            'service_type_id': services.id,
        })
        id = service_request.id

        folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
        partner_documents = request.env['documents.document'].sudo().search([('partner_id', '=', partner.id)])

        list_partner_docs = [doc.document_type_id.id for doc in list(partner_documents)]

        for docs in list(services.document_types):
            if docs.id in list_partner_docs:
                documents = request.env['documents.document'].sudo().search([('partner_id', '=', partner.id),
                                                                             ('document_type_id', '=', docs.id)],
                                                                            limit=1)
                service_request.sudo().write({'document_in': [(4, documents.id)]})
            else:
                documents = request.env['documents.document'].create({
                    'partner_id': partner.id,
                    'type': 'binary',
                    'document_type_id': docs.id,
                    'folder_id': folder.id
                })
                service_request.sudo().write({'document_in': [(4, documents.id)]})
        return {'id': id}

    @http.route(['/my/service/service_auto_save'], type='http', auth='user', website=True)
    def service_auto_save(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        service_id = request.params['service_id']
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', partner.id)])

        description = request.params['description']
        account_number = ''
        bank_name = ''
        branch = ''
        agent_address = ''
        if post.__contains__('beneficiary'):
            beneficiary = request.params['beneficiary']
            service.sudo().write({'service_beneficiary': beneficiary})

        if post.__contains__('agent_address'):
            agent_address = request.params['agent_address']
        if post.__contains__('account_number'):
            account_number = request.params['account_number']
        if post.__contains__('bank_name'):
            bank_name = request.params['bank_name']
        if post.__contains__('branch'):
            branch = request.params['branch']
        # PASSPORTS
        if service.service_type_id.code in '01-06':
            if post.__contains__('consular_number'):
                consular_number = request.params['consular_number']
            if post.__contains__('receipt_number'):
                receipt_number = request.params['receipt_number']
            release_Date = None
            if post.__contains__('release_Date'):
                release_Date = request.params['release_Date']

            service.sudo().write({'consular_number': consular_number,
                                  'receipt_number': receipt_number,
                                  'release_Date': datetime.strptime(release_Date, '%d/%m/%Y') if release_Date else None
                                  })

        if service.service_type_id.code in '04-05':
            renewal_nb = None
            if post.__contains__('renewal_nb'):
                renewal_nb = request.params['renewal_nb']
            renewal_date = None
            if post.__contains__('renewal_date'):
                renewal_date = request.params['renewal_date']
            renewal_passport_period = None
            if post.__contains__('renewal_passport_period'):
                renewal_passport_period = request.params['renewal_passport_period']
            renewal_receipt_number = None
            if post.__contains__('renewal_receipt_number'):
                renewal_receipt_number = request.params['renewal_receipt_number']
            # new_renewal_date_vals =
            service.sudo().write({'renewal_nb': renewal_nb,
                                  'renewal_date': datetime.strptime(renewal_date, '%d/%m/%Y') if renewal_date else None,
                                  'passport_period': renewal_passport_period,
                                  'receipt_number': renewal_receipt_number
                                  })
            print("------------1609------%%%%%%%%%%%%%%", renewal_date)

        if service.service_type_id.code in ('01-01', '01-02'):
            passport_period = None
            if post.__contains__('passport_period'):
                passport_period = request.params['passport_period']

            current_passport_type = None
            if post.__contains__('current_passport_type'):
                current_passport_type = request.params['current_passport_type']
            with_husband_name = False
            if post.__contains__('with_husband_name'):
                if request.params['with_husband_name'] == 'on':
                    with_husband_name = True
            dhl25 = False
            if post.__contains__('dhl25'):
                if request.params['dhl25'] == 'on':
                    dhl25 = True
            pal_doc_period = None
            if post.__contains__('pal_doc_period'):
                pal_doc_period = request.params['pal_doc_period']
            if post.__contains__('current_passport_type_pal'):
                current_passport_type = request.params['current_passport_type_pal']

            received_by = None
            if post.__contains__('received_by'):
                received_by = request.params['received_by']

            dhl30 = False
            if post.__contains__('dhl30'):
                if request.params['dhl30'] == 'on':
                    dhl30 = True
            documentNo = None
            if post.__contains__('documentNo'):
                documentNo = request.params['documentNo']
            release_Date = None
            if post.__contains__('release_Date'):
                release_Date = request.params['release_Date']

            service.sudo().write({'passport_period': passport_period,
                                  'with_husband_name': with_husband_name,
                                  'current_passport_type': current_passport_type,
                                  'dhl25': dhl25,
                                  'release_Date': datetime.strptime(release_Date, '%d/%m/%Y') if release_Date else None,
                                  'pal_doc_period': pal_doc_period,
                                  'received_by': received_by,
                                  'dhl30': dhl30,
                                  'documentNo': documentNo
                                  })

        # VISA
        if service.service_type_id.code in '04-02':
            if post.__contains__('purpose_of_trip'):
                purpose_of_trip = request.params['purpose_of_trip']
            if post.__contains__('visa_duration'):
                visa_duration = request.params['visa_duration']
            if post.__contains__('nb_entries'):
                nb_entries = request.params['nb_entries']
            if post.__contains__('entry_point'):
                entry_point = request.params['entry_point']
            if post.__contains__('expected_arrival_day'):
                expected_arrival_day = request.params['expected_arrival_day']
            if post.__contains__('expected_departure_day'):
                expected_departure_day = request.params['expected_departure_day']
            if post.__contains__('visa_no'):
                visa_no = request.params['visa_no']
            if post.__contains__('receipt_no'):
                receipt_no = request.params['receipt_no']

            service.sudo().write({'purpose_of_trip': purpose_of_trip,
                                  'visa_duration': visa_duration,
                                  'nb_entries': nb_entries,
                                  'entry_point': entry_point,
                                  'expected_arrival_day': datetime.strptime(expected_arrival_day,
                                                                            '%d/%m/%Y') if expected_arrival_day else None,
                                  'expected_departure_day': datetime.strptime(expected_departure_day,
                                                                              '%d/%m/%Y') if expected_departure_day else None,
                                  'visa_no': visa_no,
                                  'receipt_no': receipt_no})

        # Personal
        if service.service_type_id.code in ('02-02', '02-04'):
            if post.__contains__('spouse'):
                spouse = request.params['spouse']
                dependent = request.env['res.partner'].search(
                    ['&', ('id', '=', spouse), ('parent_id', '=', partner.id)])
                passport = request.env['ebs_mod.contact.passport'].search(
                    ['&', ('dependent', '=', dependent.id), ('is_active', '=', True)])
                ikama = request.env['ebs_mod.contact.ikama'].search(
                    ['&', ('dependent', '=', dependent.id), ('is_active', '=', True)])

                service.sudo().write({'spouse': dependent.id,
                                      'spouse_passport': passport.id,
                                      'spouse_ikama': ikama.id})

        if service.service_type_id.code == '02-04':
            if post.__contains__('childfirstName'):
                childfirstName = request.params['childfirstName']
            if post.__contains__('childmiddleName'):
                childmiddleName = request.params['childmiddleName']
            if post.__contains__('childlastName'):
                childlastName = request.params['childlastName']
            if post.__contains__('childfirstName_EN'):
                childfirstName_EN = request.params['childfirstName_EN']
            if post.__contains__('childmiddleName_EN'):
                childmiddleName_EN = request.params['childmiddleName_EN']
            if post.__contains__('childlastName_EN'):
                childlastName_EN = request.params['childlastName_EN']
            if post.__contains__('childdate'):
                childdate = request.params['childdate']
            if post.__contains__('childplaceOfBirth'):
                childplaceOfBirth = request.params['childplaceOfBirth']
            if post.__contains__('child_gender'):
                child_gender = request.params['child_gender']
            child_birth_certificate_date = None
            child_birth_certificate = None
            if post.__contains__('child_birth_certificate_date'):
                child_birth_certificate_date = request.params['child_birth_certificate_date']
            if child_birth_certificate_date == '':
                child_birth_certificate_date = None
            if post.__contains__('child_birth_certificate'):
                child_birth_certificate = request.params['child_birth_certificate']

            if post.__contains__('child_birth_registration'):
                child_birth_registration = request.params['child_birth_registration']
            if post.__contains__('child_birth_registration_date'):
                child_birth_registration_date = request.params['child_birth_registration_date']
            if post.__contains__('birth_registry_number'):
                birth_registry_number = request.params['birth_registry_number']
            if post.__contains__('birth_record_page'):
                birth_record_page = request.params['birth_record_page']
            if post.__contains__('record_personal_status'):
                record_personal_status = request.params['record_personal_status']
            if post.__contains__('record_transaction_number'):
                record_transaction_number = request.params['record_transaction_number']
            if post.__contains__('starting_date'):
                starting_date = request.params['starting_date']
            if post.__contains__('child_passport_number'):
                child_passport_number = request.params['child_passport_number']
            service.sudo().write({'child_birth_certificate_date': datetime.strptime(child_birth_certificate_date,
                                                                                    '%d/%m/%Y') if child_birth_certificate_date else None,
                                  'child_birth_certificate': child_birth_certificate,
                                  'child_birth_registration': child_birth_registration,
                                  'child_birth_registration_date': datetime.strptime(child_birth_certificate_date,
                                                                                     '%d/%m/%Y') if child_birth_registration_date else None,
                                  'birth_registry_number': birth_registry_number,
                                  'birth_record_page': birth_record_page,
                                  'record_personal_status': record_personal_status,
                                  'record_transaction_number': record_transaction_number,
                                  'starting_date': datetime.strptime(starting_date,
                                                                     '%d/%m/%Y') if starting_date else None,
                                  'child_passport_number': child_passport_number})
            dependent_type = 'child'
            name = childfirstName + ' ' + childmiddleName + ' ' + childlastName
            dependent = service.child

            if not dependent:
                dependent = request.env['res.partner'].create({
                    'name': name,
                    'firstName': childfirstName,
                    'middleName': childmiddleName,
                    'lastName': childlastName,
                    'first_name_en': childfirstName_EN,
                    'middle_name_en': childmiddleName_EN,
                    'last_name_en': childlastName_EN,
                    'dependent_type': dependent_type,
                    'gender': child_gender,
                    'person_type': 'child',
                    'parent_id': partner.id,
                    'placeOfBirth': childplaceOfBirth,
                    'date': datetime.strptime(childdate, '%d/%m/%Y') if childdate else None,
                })

                service.sudo().write({'child': dependent})
            else:
                dependent.write({
                    'name': name,
                    'firstName': childfirstName,
                    'middleName': childmiddleName,
                    'lastName': childlastName,
                    'first_name_en': childfirstName_EN,
                    'middle_name_en': childmiddleName_EN,
                    'last_name_en': childlastName_EN,
                    'placeOfBirth': childplaceOfBirth,
                    'date': datetime.strptime(childdate, '%d/%m/%Y') if childdate else None,
                    'gender': child_gender,
                })

        if service.service_type_id.code in ('02-01', '02-03'):
            if post.__contains__('depfirstName'):
                depfirstName = request.params['depfirstName']
            if post.__contains__('depmiddleName'):
                depmiddleName = request.params['depmiddleName']
            if post.__contains__('deplastName'):
                deplastName = request.params['deplastName']
            if post.__contains__('depfirstName_EN'):
                depfirstName_EN = request.params['depfirstName_EN']
            if post.__contains__('depmiddleName_EN'):
                depmiddleName_EN = request.params['depmiddleName_EN']
            if post.__contains__('deplastName_EN'):
                deplastName_EN = request.params['deplastName_EN']
            if post.__contains__('depdate'):
                depdate = request.params['depdate']
            if post.__contains__('depplaceOfBirth'):
                depplaceOfBirth = request.params['depplaceOfBirth']
            if post.__contains__('depkazaBirth'):
                depkazaBirth = request.params['depkazaBirth']
            if post.__contains__('depsejelNo'):
                depsejelNo = request.params['depsejelNo']
            if post.__contains__('depnationality'):
                depnationality = request.params['depnationality']
            if depnationality == '':
                depnationality = None
            else:
                depnationality = int(depnationality)

            if post.__contains__('depsec_natio'):
                depsec_natio = request.params['depsec_natio']

            if depsec_natio == '':
                depsec_natio = None
            else:
                depsec_natio = int(depsec_natio)
            if post.__contains__('depreligion'):
                depreligion = request.params['depreligion']
            if post.__contains__('occupation'):
                occupation = request.params['occupation']
            if post.__contains__('depfather_fullname'):
                depfather_fullname = request.params['depfather_fullname']
            if post.__contains__('depmotherFullName'):
                depmotherFullName = request.params['depmotherFullName']
            dependent_type = 'spouse'
            name = depfirstName + ' ' + depmiddleName + ' ' + deplastName
            dependent = service.spouse

            if not dependent:
                vals = {
                    'name': name,
                    'firstName': depfirstName,
                    'middleName': depmiddleName,
                    'lastName': deplastName,
                    'first_name_en': depfirstName_EN,
                    'middle_name_en': depmiddleName_EN,
                    'last_name_en': deplastName_EN,
                    'dependent_type': dependent_type,
                    'person_type': 'child',
                    'parent_id': partner.id,
                    'nationality': depsec_natio,
                    'country_id': depnationality,
                    'sejelNo': depsejelNo,
                    'function': occupation,
                    'motherFullName': depmotherFullName,
                    'placeOfBirth': depplaceOfBirth,
                    'date': datetime.strptime(depdate, '%d/%m/%Y') if depdate else None,
                    'father_fullname': depfather_fullname,
                    'kazaBirth': depkazaBirth,
                    'religion': depreligion
                }
                dependent = request.env['res.partner'].create(vals)
                service.sudo().write({'spouse': dependent})

            else:
                dependent.write({
                    'name': name,
                    'firstName': depfirstName,
                    'middleName': depmiddleName,
                    'lastName': deplastName,
                    'first_name_en': depfirstName_EN,
                    'middle_name_en': depmiddleName_EN,
                    'last_name_en': deplastName_EN,
                    'nationality': depsec_natio,
                    'country_id': depnationality,
                    'sejelNo': depsejelNo,
                    'function': occupation,
                    'motherFullName': depmotherFullName,
                    'placeOfBirth': depplaceOfBirth,
                    'date': datetime.strptime(depdate, '%d/%m/%Y') if depdate else None,
                    'father_fullname': depfather_fullname,
                    'kazaBirth': depkazaBirth,
                    'religion': depreligion
                })

            if service.service_type_id.code in '02-03':
                if post.__contains__('depmarriage_date'):
                    depmarriage_date = request.params['depmarriage_date']
                if post.__contains__('depmarriage_place'):
                    depmarriage_place = request.params['depmarriage_place']

                dependent.sudo().write(
                    {'marriage_date': datetime.strptime(depmarriage_date, '%d/%m/%Y') if depmarriage_date else None,
                     'marriage_place': depmarriage_place})

            if post.__contains__('passport_no'):
                passport_no = request.params['passport_no']
            if post.__contains__('passport_place'):
                passport_place = request.params['passport_place']
            if post.__contains__('passport_start_date'):
                passport_start_date = request.params['passport_start_date']
            if passport_start_date == '':
                passport_start_date = None
            if post.__contains__('passport_exp_date'):
                passport_exp_date = request.params['passport_exp_date']
            if passport_exp_date == '':
                passport_exp_date = None

            passport = service.spouse_passport
            if not passport.id:
                passport = request.env['ebs_mod.contact.passport'].create({
                    'passport_no': passport_no,
                    'passport_place': passport_place,
                    'passport_start_date': passport_start_date,
                    'passport_exp_date': passport_exp_date,
                    'is_active': True,
                    'partner_id': partner.id,
                    'family_member': 'spouse',
                    'dependent': dependent.id
                })
                service.sudo().write({'spouse_passport': passport.id})
            else:
                passport.write({
                    'passport_no': passport_no,
                    'passport_place': passport_place,
                    'passport_start_date': datetime.strptime(passport_start_date,
                                                             '%d/%m/%Y') if passport_start_date else None,
                    'passport_exp_date': datetime.strptime(passport_exp_date,
                                                           '%d/%m/%Y') if passport_exp_date else None,
                    'is_active': True
                })

            if post.__contains__('ikama_no'):
                ikama_no = request.params['ikama_no']
            if post.__contains__('ikama_enddate'):
                ikama_enddate = request.params['ikama_enddate']
            if post.__contains__('guarantor'):
                guarantor = request.params['guarantor']

            ikama = service.spouse_ikama
            if not ikama.id:
                ikama = request.env['ebs_mod.contact.ikama'].create({
                    'ikama_enddate': datetime.strptime(ikama_enddate, '%d/%m/%Y') if ikama_enddate else None,
                    'ikama_no': ikama_no,
                    'dependent': dependent.id,
                    'guarantor': guarantor,
                    'occupation': occupation,
                    'is_active': True,
                    'partner_id': partner.id,
                    'family_member': 'spouse'
                })
                service.sudo().write({'spouse_ikama': ikama.id})
            else:
                ikama.write({
                    'ikama_enddate': datetime.strptime(ikama_enddate, '%d/%m/%Y') if ikama_enddate else None,
                    'ikama_no': ikama_no,
                    'guarantor': guarantor,
                    'occupation': occupation,
                    'is_active': True
                })

        service.sudo().write({
            'desc': description,
            'account_number': account_number,
            'bank_name': bank_name,
            'branch': branch,
            'agent_address': agent_address
        })
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': service.id}
        }), headers=headers)

    @http.route(['/my/service/submit_feedback'], type='http', auth="user", website=True)
    def contact_service_submit_feedback(self, **post):
        headers = [('Content-Type', 'application/json')]
        user = request.env.user
        partner = user.partner_id
        today = date.today()
        if post.get('rating') or post.get('comments'):
            if post.get('rating') == '2.56':
                rating = None
            else:
                rating = post.get('rating')
            service_feedback = request.env['ebs_mod.service.request.feedback'].create({
                'rating': rating,
                'comments': post.get('comments'),
                'service_id': post.get('service_id'),
            })

        print(post, "@@@@@@@@@@@@")
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': post.get('service_id')},
            'type': 'auth',
        }), headers=headers)

    @http.route(['/my/mou3amalt_konsoliya', '/my/mou3amalt_konsoliya/page/<int:page>'], type='http'
        , auth="public", website=True)
    def my_contact_mou3amalt_konsoliya(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                                       search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            # 'date': {'label': _('Newest'), 'order': 'create_date desc'},
            # 'date_desc': {'label': _('Oldest'), 'order': 'create_date asc'},
        }
        searchbar_inputs = {
            # 'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        # order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/mou3amalt_konsoliya",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        mou3amalt_konsoliya = request.env['ebs_mod.service.types'].sudo().search([('path', '=', '/mou3amalt_konsoliya')],
                                                                          limit=1)
        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        mou3amalt_konsoliya_services = request.env['ebs_mod.service.types'].sudo().search(
            [('parent_service_id', '=', int(mou3amalt_konsoliya.id)),
             '|', ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page)

        request.session['my_mou3amalt_konsoliya_history'] = mou3amalt_konsoliya.ids[:100]
        values.update({
            'date': date_begin,
            'mou3amalt_konsoliya': mou3amalt_konsoliya,
            'mou3amalt_konsoliya_services': mou3amalt_konsoliya_services,
            'page_name': 'mou3amalt_konsoliya',
            'default_url': '/my/mou3amalt_konsoliya',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })

        if not request.env.user.has_group('base.group_public'):
            return request.render("ebs_qsheild_mod.portal_contact_mou3amalt_konsoliya", values)
        else:
            mou3amalt_konsoliya_services = request.env['ebs_mod.service.types'].sudo().search(
                [('parent_service_id', '=', int(mou3amalt_konsoliya.id)),
                 '|', ('for_lebanese', '=', True)
                    , ('for_palestinian', '=', True)]
                , limit=self._items_per_page)
            return request.render("ebs_qsheild_mod.portal_logout_contact_passports",
                                  {'passports_services': mou3amalt_konsoliya_services})

    @http.route(['/my/ifadat', '/my/ifadat/page/<int:page>'], type='http'
        , auth="user", website=True)
    def my_contact_ifadat(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                          search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'date asc'},
        }
        searchbar_inputs = {
            'status': {'input': 'status', 'label': _('Status')},
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        s_domain = []
        if search and search_in:
            search_domain = []
            if search_in == 'status':
                search_domain = OR([search_domain, [('status', 'ilike', search)]])
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            s_domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].search_count(domain)
        pager = portal_pager(
            url="/my/ifadat",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True
        ifadat = request.env['ebs_mod.service.types'].search([('path', '=', '/ifadat')]
                                                             , limit=1
                                                             )
        ifadat_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(ifadat.id)),
             '|', ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)]
            , limit=self._items_per_page
        )

        child_service = [serv.id for serv in list(ifadat_services)]

        s_domain.append(('partner_id', '=', user.partner_id.id))
        s_domain.append(('service_type_id', 'in', child_service))
        service_request = request.env['ebs_mod.service.request'].search(s_domain, offset=pager['offset'], order=order)

        request.session['my_ifadat_services_history'] = ifadat_services.ids[:100]
        values.update({
            'date': date_begin,
            'ifadat_services': ifadat_services,
            'service_request': service_request,
            'page_name': 'ifadat',
            'default_url': '/my/ifadat',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        return request.render("ebs_qsheild_mod.portal_contact_2ifadat", values)

    @http.route(['/my/tasdkiat', '/my/tasdkiat/page/<int:page>'], type='http'
        , auth="user", website=True)
    def my_contact_tasdikat(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
                            search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'date asc'},
        }
        searchbar_inputs = {
            'status': {'input': 'status', 'label': _('Status')},
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        s_domain = []
        if search and search_in:
            search_domain = []
            if search_in == 'status':
                search_domain = OR([search_domain, [('status', 'ilike', search)]])
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            s_domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].search_count(domain)
        pager = portal_pager(
            url="/my/tasdkiat",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        isLebanese = False
        isPalestinian = False
        if user.partner_id.first_Nationality == 'leb':
            isLebanese = True
        else:
            if user.partner_id.first_Nationality == 'pal':
                isPalestinian = True

        tasdikat = request.env['ebs_mod.service.types'].search([('path', '=', '/tasdkiat')]
                                                               , limit=1)

        tasdikat_services = request.env['ebs_mod.service.types'].search(
            [('parent_service_id', '=', int(tasdikat.id)),
             '|', ('for_lebanese', '=', isLebanese)
                , ('for_palestinian', '=', isPalestinian)], limit=self._items_per_page)

        child_service = [serv.id for serv in list(tasdikat_services)]

        s_domain.append(('partner_id', '=', user.partner_id.id))
        s_domain.append(('service_type_id', 'in', child_service))
        service_request = request.env['ebs_mod.service.request'].search(s_domain, offset=pager['offset'], order=order)

        request.session['my_tasdikat_history'] = tasdikat_services.ids[:100]
        values.update({
            'date': date_begin,
            'tasdikat_services': tasdikat_services,
            'service_request': service_request,
            'page_name': 'tasdikat',
            'default_url': '/my/tasdkiat',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        return request.render("ebs_qsheild_mod.portal_contact_tasdikat", values)

    @http.route(['/my/tasdikat/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_tasdikat_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None
        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            document_type = document.document_type_id
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        # tasdikat_insert
        values = {
            'page_name': 'tasdikat_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }

        return request.render("ebs_qsheild_mod.portal_contact_tasdikat_form", values)

    @http.route(['/my/ifadat/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_ifadat_document(self, **post):
        partner_doc_Id = request.params['partner_doc_Id']
        docNo = request.params['docNo'] or None
        issueDate = request.params['issueDate'] or None
        expiryDate = request.params['expiryDate'] or None
        file = request.params['files[]']
        service_id = request.params['service_id']
        user = request.env.user
        service = request.env['ebs_mod.service.request'].search(
            [('id', '=', service_id), ('partner_id', '=', user.partner_id.id)])

        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })

        if partner_doc_Id:
            document = request.env['documents.document'].search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            document_type = document.document_type_id
        elif not partner_doc_Id and post.__contains__('document_type'):
            doc_type = request.params['document_type']
            document_type = request.env['ebs_mod.document.types'].search([('id', '=', doc_type)])

            folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
            document = request.env['documents.document'].create({
                'type': 'binary',
                'document_type_id': document_type.id,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': user.partner_id.id,
                'folder_id': folder.id,
            })
            service.sudo().write({'document_in': [(4, document.id)]})

        doc = service.document_in
        # ifadat_insert
        values = {
            'page_name': 'ifadat_insert',
            'service_request': service,
            'documents': doc,
            'partner': user.partner_id,
            'documentTypes': request.env['ebs_mod.document.types'].sudo().search([]),
            'kadaa': request.env['ebs_mod.country.kaza'].sudo().search([]),
            'religion': request.env['ebs_mod.contact.religion'].sudo().search([]),
            'countries': request.env['res.country'].sudo().search([]),
        }

        return request.render("ebs_qsheild_mod.portal_contact_ifadat_form", values)

    @http.route(['/my/ifadat/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_ifadat_insert_doc_form(self, id):
        user = request.env.user
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open Request."))
        documents = service_request.document_in
        documentTypes = request.env['ebs_mod.document.types'].sudo().search([])

        values = {
            'page_name': 'ifadat_insert',
            'service_request': service_request,
            'documents': documents,
            'documentTypes': documentTypes
        }

        return request.render("ebs_qsheild_mod.portal_contact_ifadat_form", values)

    @http.route(['/my/tasdikat/insert_doc_form/<int:id>'], type='http', auth='user', website=True)
    def contact_tasdikat_insert_doc_form(self, id,**kw):
        print(".........kw..........",kw,id)
        user = request.env.user
        service_request = request.env['ebs_mod.service.request'].search(
            [('id', '=', id), ('partner_id', '=', user.partner_id.id)])
        if len(service_request) == 0:
            raise ValidationError(_("Cannot Open Request."))
        documentTypes = request.env['ebs_mod.document.types'].sudo().search([])
        # nationality_ids = request.env['res.country'].sudo().search([])
        documents = service_request.document_in
        values = {
            'page_name': 'tasdikat_insert',
            'service_request': service_request,
            'documents': documents,
            'documentTypes': documentTypes,
        # 'nationality_ids':nationality_ids,
        }

        return request.render("ebs_qsheild_mod.portal_contact_tasdikat_form", values)

    @http.route(['/my/payments', '/my/payments/page/<int:page>'], type='http', auth="user", website=True)
    def my_contact_payment(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='content',
                           **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'date_desc': {'label': _('Oldest'), 'order': 'create_date asc'},
        }
        searchbar_inputs = {
            'desc': {'input': 'desc', 'label': _('Description')}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = []
        # archive_groups = self._get_archive_groups('ebs_mod.contact.payment', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'desc':
                search_domain = OR([search_domain, [('desc', 'ilike', search)]])
            domain += search_domain

        # pager
        payment_count = request.env['ebs_mod.contact.payment'].search_count(domain)
        pager = portal_pager(
            url="/my/payments",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        payments = request.env['ebs_mod.contact.payment'].search(domain, order=order, limit=self._items_per_page,
                                                                 offset=pager['offset'])
        request.session['my_payments_history'] = payments.ids[:100]
        values.update({
            'date': date_begin,
            'payments': payments,
            'page_name': 'payment',
            'default_url': '/my/payments',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        return request.render("ebs_qsheild_mod.portal_contact_payment", values)

    @http.route(['/my/payments/insert_form'], type='http', auth='user', website=True)
    def contact_payment_insert_form(self):

        values = {
            'page_name': 'payment_insert',
            'currency': request.env.company.currency_id
        }

        return request.render("ebs_qsheild_mod.portal_contact_payment_form", values)

    @http.route(['/my/payments/return_url'], type='http', auth='user', method=['GET'], website=True)
    def payments_return_url(self, **kw):
        amount = request.params['vpc_Amount']
        order_info = request.params['vpc_OrderInfo']
        message = request.params['vpc_Message']
        trx_response_code = request.params.get('vpc_TxnResponseCode', False)
        vpc_receipt_no = request.params.get('vpc_ReceiptNo', False)
        acq_response_code = request.params.get('vpc_AcqResponseCode', False)
        transaction_no = request.params.get('vpc_TransactionNo', False)
        batch_no = request.params.get('vpc_BatchNo', False)
        authorize_id = request.params.get('vpc_AuthorizeId', False)

        transaction = request.env['ebs_mod.payment.transaction'].search([('order_info', '=', order_info)],
                                                                        limit=1)
        vals = {
            'message': message
        }
        if trx_response_code:
            vals['trx_response_code_full'] = trx_response_code
            if trx_response_code[0] == '0':
                vals['trx_response_code'] = '0'
            else:
                vals['trx_response_code'] = '1'
        else:
            vals['trx_response_code_full'] = '1'
            vals['trx_response_code'] = '1'

        if acq_response_code:
            vals['acq_response_code'] = acq_response_code
        if transaction_no:
            vals['transaction_no'] = transaction_no
        if vpc_receipt_no:
            vals['vpc_receipt_no'] = vpc_receipt_no
        if batch_no:
            vals['batch_no'] = batch_no
        if authorize_id:
            vals['authorize_id'] = authorize_id

        transaction.sudo().write(vals)

        if transaction.trx_response_code == "0":
            request.env['ebs_mod.contact.payment'].create({
                "transaction_id": transaction.id
            })

        return request.redirect('/my/payments')

    @http.route(['/my/payments/secure_token'], type='http', auth='user', method=['GET'], website=True)
    def payment_secure_token(self, **kw):
        with_token = False
        if request.params.get('token', False):
            if len(request.params['token']) == 51:
                with_token = True
        if with_token:
            env = request.env
            amount1 = request.params['amount1']
            amount2 = request.params['amount2']
            x = re.search("^[0 9]{2}$", amount2)
            if not x:
                return json.dumps({'status': "error", 'msg': _("Second field must be 2 digits only")})

            y = re.search("^\d+$", amount1)
            if not y:
                return json.dumps({'status': "error", 'msg': _("First field must be digits only")})

            amount = str(amount1) + str(amount2)
            host_url = request.httprequest.host_url
            # w = re.search("localhost", host_url)
            # if not x:
            return_url = host_url + "my/payments/return_url"
            # return_url = "http://jaafarkhansa.com/demo/gateway/index.php"
            # else:
            #     return_url = "http://jaafarkhansa.com/demo/gateway/index.php"
            transaction = env['ebs_mod.payment.transaction'].sudo().create(
                {
                    "partner_id": request.env.user.partner_id.id,
                    "currency_id": env['res.currency'].search([('name', '=', 'QAR')], limit=1).id,
                    "amount": (float(amount) / 100.0),
                    "date": datetime.today()
                }
            )

            api_secret = "AB563B8F4E9DB457F52E3D77F214C977"
            message = "vpc_AccessCode=E8AEDBAA"
            message += "&vpc_Amount=" + amount
            message += "&vpc_Command=pay"
            message += "&vpc_Currency=QAR"
            message += "&vpc_Locale=en"
            message += "&vpc_MerchTxnRef=txn1"
            message += "&vpc_Merchant=DB91363"
            message += "&vpc_OrderInfo=" + transaction.order_info
            message += "&vpc_ReturnURL=" + return_url
            message += "&vpc_Version=1"
            signature = hmac.new(binascii.unhexlify(bytes(api_secret, 'UTF-8')),
                                 msg=message.encode("UTF-8"),
                                 digestmod=hashlib.sha256).hexdigest().upper()

            return json.dumps({
                'status': "success",
                'data': {'key': signature,
                         'order_id': transaction.order_info,
                         'return_url': return_url
                         }
            })
        else:
            return json.dumps({'status': "error", 'msg': _("Token Error")})

    @http.route(['/my/payments/insert'], type='http', auth='user', website=True)
    def contact_payment_insert(self):

        request.env['ebs_mod.contact.payment'].create({
            'partner_id': request.env.user.partner_id.id,
            'amount': float(request.params['amount']),
            'currency_id': int(request.params['currency']),
            'desc': request.params['desc'],
        })
        return self.contact_payment_insert_form()


class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        # values['ticket_count'] = request.env['helpdesk.ticket'].search_count(
        #     [('partner_id', '=', request.env.user.partner_id.id)])
        if values.get('sales_user', False):
            values['title'] = _("Salesperson")
        return values

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='content',
                            **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('partner_id', '=', user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Subject'), 'order': 'name'},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'id': {'input': 'id', 'label': _('Search ID')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('helpdesk.ticket', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            domain += search_domain

        # pager
        tickets_count = request.env['helpdesk.ticket'].search_count(domain)
        pager = portal_pager(
            url="/my/tickets",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=tickets_count,
            page=page,
            step=self._items_per_page
        )

        tickets = request.env['helpdesk.ticket'].search(domain, order=order, limit=self._items_per_page,
                                                        offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]

        values.update({
            'date': date_begin,
            'tickets': tickets,
            'page_name': 'ticket',
            'default_url': '/my/tickets',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        return request.render("helpdesk.portal_helpdesk_ticket", values)

    @http.route(['/my/account/save_image'], type='http', auth='user', method=['GET', 'POST'], website=True)
    def save_image(self, **kw):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id

        values = {}
        if kw.get('image_1920') and kw.get('image_1920') != '':
            u_f = kw.get('image_1920')
            values.update({'image_1920': u_f.split(',')[1].encode('utf-8')})
        partner.sudo().write(values)

        return request.make_response(json.dumps({
            'status': "success",
            'msg': _('Successfully Submitted'),
            'data': {'msg': _('Successfully Submitted')}
        }), headers=headers)

    @http.route(['/my/account/submit'], type='http', auth='user', method=['GET', 'POST'], website=True)
    def contact_submit(self, **kw):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        print("image>>>>>>", kw.get('image_1920'))
        values = {}
        vals = {}
        country_id = values.get('country_id') or 126
        if values.get('country_id') == '':
            country_id = 126

        values.update({'country_id': int(country_id)})

        # p_file = request.params.get('im_image')
        # print("pfff>>>", p_file, kw)
        # if p_file is not None and p_file is not '':
        #     values.update({'image_1920': base64.b64encode(p_file.read())})
        # attachment_64 = request.env['ir.attachment'].create({
        #     'name': file.filename,
        #     'datas': base64.b64encode(file.read()),
        #     'type': 'binary',
        # })

        if kw.get('image_1920') and kw.get('image_1920') != '':
            u_f = kw.get('image_1920')
            # values.update({'image_1920': bytes(u_f).replace("b'\n',b")})
            values.update({'image_1920': u_f.split(',')[1].encode('utf-8')})

        name = request.params['firstName'] + ' ' + request.params['middleName'] + ' ' + request.params[
            'lastName']
        values.update({'name': name})

        values.update({'person_type': 'emp'})

        first_Nationality = request.params['first_Nationality']
        if first_Nationality == '':
            first_Nationality = None
        values.update({'first_Nationality': first_Nationality})

        values.update({'firstName': request.params['firstName']})
        values.update({'middleName': request.params['middleName']})
        values.update({'lastName': request.params['lastName']})
        values.update({'motherFullName': request.params['motherFullName']})
        values.update({'kazaBirth': request.params['kazaBirth']})
        values.update({'placeOfBirth': request.params['placeOfBirth']})

        values.update({'first_name_en': request.params['firstName_EN']})
        values.update({'middle_name_en': request.params['middleName_EN']})
        values.update({'last_name_en': request.params['lastName_EN']})
        values.update({'mother_full_name_en': request.params['motherFullName_EN']})
        values.update({'place_of_birth_en': request.params['placeOfBirth_EN']})
        values.update({'father_fullname_en': request.params['father_fullname_en']})

        date_of_birth = request.params['date_of_birth']
        if date_of_birth == '':
            date_of_birth = None
            vals = {'date': datetime.strptime(date_of_birth, '%d/%m/%Y') if date_of_birth else None}
        values.update(vals)

        values.update({'birth_certificate_nb': request.params['birth_certificate_nb']})

        birth_certificate_date = request.params['birth_certificate_date']
        if birth_certificate_date == '':
            birth_certificate_date = None
            vals = {'birth_certificate_date': datetime.strptime(birth_certificate_date,
                                                                '%d/%m/%Y') if birth_certificate_date else None}
        values.update(vals)

        maritalStatus = request.params['maritalStatus']
        if maritalStatus == '':
            maritalStatus = None
        values.update({'maritalStatus': maritalStatus})
        values.update({'gender': request.params['gender']})
        values.update({'sejelNo': request.params['sejelNo']})
        values.update({'sejel_place': request.params['sejel_place']})

        values.update({'id_no': request.params['id_no']})
        values.update({'stati_no': request.params['stati_no']})
        values.update({'registered_with': request.params['registered_with']})

        nationality = request.params['nationality']
        if nationality == '':
            nationality = None

        values.update({'nationality': nationality})

        qatarfirstvisit_date = request.params['qatarfirstvisit_date']
        qatarfirstvisit = {}
        if qatarfirstvisit_date == '':
            qatarfirstvisit_date = None
            qatarfirstvisit = {'qatarfirstvisit_date': datetime.strptime(qatarfirstvisit_date,
                                                                         '%d/%m/%Y') if qatarfirstvisit_date else None}
        values.update(qatarfirstvisit)

        values.update({'function': request.params['function']})

        values.update({'father_fullname': request.params['father_fullname']})
        values.update({'father_place_of_birth': request.params['father_place_of_birth']})

        father_date_of_birth = request.params['father_date_of_birth']
        father_date_info = {}

        if father_date_of_birth == '':
            father_date_of_birth = None
            father_date_info = {'father_date_of_birth': datetime.strptime(father_date_of_birth,
                                                                          '%d/%m/%Y') if father_date_of_birth else None}
        values.update(father_date_info)

        father_religion = request.params['father_religion']
        if father_religion == '':
            father_religion = None
        values.update({'father_religion': father_religion})
        values.update({'father_file_no': request.params['father_file_no']})
        values.update({'file_no': request.params['file_no']})
        values.update({'father_stati_no': request.params['father_stati_no']})
        values.update({'father_registered_with': request.params['father_registered_with']})
        values.update({'mother_place_of_birth': request.params['mother_place_of_birth']})

        mother_date_of_birth = request.params['mother_date_of_birth']
        mother_date = {}
        if mother_date_of_birth == '':
            mother_date_of_birth = None
            mother_date = {'mother_date_of_birth': datetime.strptime(mother_date_of_birth,
                                                                     '%d/%m/%Y') if mother_date_of_birth else None}
        values.update(mother_date)
        print("---------mother date new-----", mother_date)
        religion = request.params['religion']
        if religion == '':
            religion = None
        values.update({'religion': religion})

        mother_religion = request.params['mother_religion']
        if mother_religion == '':
            mother_religion = None
        values.update({'mother_religion': mother_religion})
        values.update({'mother_file_no': request.params['mother_file_no']})
        values.update({'mother_stati_no': request.params['mother_stati_no']})
        values.update({'mother_registered_with': request.params['mother_registered_with']})

        partner.sudo().write(values)
        required_documents = False

        isLebanese = False
        isPalestinian = False
        if partner.first_Nationality == 'leb':
            isLebanese = True
            required_documents = request.env['ebs_mod.document.types'].search([('is_mandatory', '=', True)
                                                                                  , ('for_lebanese', '=', isLebanese)
                                                                               ])
        elif partner.first_Nationality == 'pal':
            isPalestinian = True
            required_documents = request.env['ebs_mod.document.types'].search([('is_mandatory', '=', True),
                                                                               ('for_palestinian', '=', isPalestinian)])
        else:
            required_documents = request.env['ebs_mod.document.types'].sudo().search([('is_required', '=', True),
                                                                                      ('for_lebanese', '=', False),
                                                                                      ('for_palestinian', '=', False)])
        partner_docs = list(partner.document_o2m)

        check_doc = True
        for doc in partner_docs:
            if doc.document_type_id in required_documents:
                if not doc.attachment_id:
                    check_doc = False

        message = ''
        if check_doc is False:
            message = _('Please make sure that all required documents listed below are attached:\n')
            message = message + '<br/>'

            for doc in required_documents:
                message = message + doc.name + '<br/>'
        message = message + '<br/>'
        check_req_fields = True

        # if len(partner.contact_passports) == 0:
        #     message = _('**Make sure to add passport details ') + '<br/>'
        #
        # if len(partner.contact_ikama) == 0:
        #     message = _('**Make sure to add Ikama details ') + '<br/>'
        #
        # if len(partner.contact_emergency) == 0:
        #     message = _('**Make sure to add Emergency details ')
        #
        # if len(list(partner.address_ids)) < 3:
        #     message = _('**Make sure to add Company, Lebanon and Qatar addresses ')

        fields = ''

        if not partner.first_Nationality or partner.first_Nationality is None or partner.first_Nationality == '':
            check_req_fields = False
            fields = fields + _('Nationality,  ') + '\n'

        if not partner.firstName or partner.firstName is None or partner.firstName == '':
            check_req_fields = False
            fields = fields + _('First Name, ') + '\n'

        if not partner.middleName or partner.middleName is None or partner.lastName == '':
            check_req_fields = False
            fields = fields + _('Middle Name, ') + '\n'

        if not partner.lastName or partner.lastName is None or partner.lastName == '':
            check_req_fields = False
            fields = fields + _('Last Name, ') + '\n'

        if not partner.first_name_en or partner.first_name_en is None or partner.first_name_en == '':
            check_req_fields = False
            fields = fields + _('First Name English  , ') + '\n'

        if not partner.middle_name_en or partner.middle_name_en is None or partner.middle_name_en == '':
            check_req_fields = False
            fields = fields + _('Middle Name English  , ') + '\n'

        if not partner.last_name_en or partner.last_name_en is None or partner.last_name_en == '':
            check_req_fields = False
            fields = fields + _('Last Name English  , ') + '\n'

        if not partner.mother_full_name_en or partner.mother_full_name_en is None or partner.mother_full_name_en == '':
            check_req_fields = False
            fields = fields + _('Mother Full Name English, ') + '\n'

        if not partner.motherFullName or partner.motherFullName is None or partner.motherFullName == '':
            check_req_fields = False
            fields = fields + _('Mother Full Name, ') + '\n'

        if not partner.placeOfBirth or partner.placeOfBirth is None or partner.placeOfBirth == '':
            check_req_fields = False
            fields = fields + _('PlaceOf Birth  , ') + '\n'

        if not partner.place_of_birth_en or partner.place_of_birth_en is None or partner.place_of_birth_en == '':
            check_req_fields = False
            fields = fields + _('Place of Birth English, ') + '\n'

        if partner.date is None:
            check_req_fields = False
            fields = fields + _('Birth Date ') + '\n'

        if not partner.maritalStatus or partner.maritalStatus is None or partner.maritalStatus == '':
            check_req_fields = False
            fields = fields + _('marital Status, ') + '\n'

        if not partner.gender or partner.gender is None or partner.gender == '':
            check_req_fields = False
            fields = fields + _('Gender, ') + '\n'

        if isLebanese:
            # if not partner.id_no or partner.id_no is None or partner.id_no == '':
            #     check_req_fields = False
            #     fields = fields + _('id no, ') + '\n'
            if not partner.sejelNo or partner.sejelNo is None or partner.sejelNo == '':
                check_req_fields = False
                fields = fields + _('sejel No, ') + '\n'

            if not partner.sejel_place or partner.sejel_place is None or partner.sejel_place == '':
                check_req_fields = False
                fields = fields + _('sejel Place, ') + '\n'


            if not partner.religion or partner.religion is None or partner.religion == '':
                check_req_fields = False
                fields = fields + _('Religion, ') + '\n'

            if not partner.kazaBirth or partner.kazaBirth is None or partner.kazaBirth == '':
                check_req_fields = False
                fields = fields + _('kaza Birth , ') + '\n'

        if isPalestinian:
            if not partner.stati_no or partner.stati_no is None or partner.stati_no == '':
                check_req_fields = False
                fields = fields + _('stati No, ') + '\n'

            if not partner.registered_with or partner.registered_with is None or partner.registered_with == '':
                check_req_fields = False
                fields = fields + _('registered with, ') + '\n'

        if not check_req_fields:
            if len(message) < 250:
                message = _('Make sure that below fields are filled: ') + '<br/>' + fields + '<br/>'
            else:
                message = _('**Make sure that all fields are filled ') + '<br/>'

        if check_doc and check_req_fields and partner.person_type != '' and partner.person_type is not None:
            if partner.email:
                ctx = {}
                ctx['subject'] = 'Application Confirm'
                ctx['email_from'] = self.env.user.company_id.email
                ctx['email_to'] = self.email
                ctx['author_id'] = self.env.user.partner_id.id
                self.env.ref("ebs_qsheild_mod.confirm_email").sudo().with_context(ctx).send_mail(self.id,email_values={'res_id':None})
                partner.sudo().write({'status': 'confirm'})

            return request.make_response(json.dumps({
                'status': "success",
                'msg': _('Successfully Submitted'),
                'data': {'msg': _('Successfully Submitted')}
            }), headers=headers)
        else:
            return request.make_response(json.dumps({
                'status': "error",
                'msg': message}), headers=headers)

    @http.route(['/my/account', '/my/account/<path:tab>'], type='http', auth='user', method=['GET'], website=True)
    def account(self, redirect=None, tab='qatar', **post):
        headers = [('Content-Type', 'application/json')]

        print("Startingggggggggggggggggggggggggg", post)

        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        vals = {}

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)

            if True:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})

                if values.get('country_id'):
                    country_id = int(values.get('country_id'))
                if values.get('country_id') == '' or not values.get('country_id'):
                    country_id = 126

                values.update({'country_id': country_id})
                values.update({'zip': values.pop('zipcode', '')})
                values.update({'state_id': 100})

                if values.get('state_id') == '':
                    values.update({'state_id': False})

                name = request.params['firstName'] + ' ' + request.params['middleName'] + ' ' + request.params[
                    'lastName']
                values.update({'name': name})
                values.update({'status': 'draft'})

                values.update({'person_type': 'emp'})
                if post.get('image_1920') and post.get('image_1920') != '':
                    u_f = post.get('image_1920')
                    # values.update({'image_1920': bytes(u_f).replace("b'\n',b")})
                    values.update({'image_1920': u_f.split(',')[1].encode('utf-8')})
                    print("image")

                first_Nationality = request.params['first_Nationality']
                if first_Nationality == '':
                    first_Nationality = None
                values.update({'first_Nationality': first_Nationality})

                values.update({'firstName': request.params['firstName']})
                values.update({'middleName': request.params['middleName']})
                values.update({'lastName': request.params['lastName']})
                values.update({'motherFullName': request.params['motherFullName']})
                values.update({'kazaBirth': request.params['kazaBirth']})
                values.update({'placeOfBirth': request.params['placeOfBirth']})

                values.update({'first_name_en': request.params['firstName_EN']})
                values.update({'middle_name_en': request.params['middleName_EN']})
                values.update({'last_name_en': request.params['lastName_EN']})
                values.update({'mother_full_name_en': request.params['motherFullName_EN']})
                values.update({'place_of_birth_en': request.params['placeOfBirth_EN']})

                date_of_birth = request.params['date_of_birth']
                if date_of_birth == '':
                    date_of_birth = None
                vals = {'date': datetime.strptime(date_of_birth, '%d/%m/%Y') if date_of_birth else None}
                values.update(vals)

                values.update({'birth_certificate_nb': request.params['birth_certificate_nb']})

                birth_certificate_date = request.params['birth_certificate_date']
                if birth_certificate_date == '':
                    birth_certificate_date = None
                vals = {'birth_certificate_date': datetime.strptime(birth_certificate_date,
                                                                    '%d/%m/%Y') if birth_certificate_date else None}
                values.update(vals)

                maritalStatus = request.params['maritalStatus']
                if maritalStatus == '':
                    maritalStatus = None
                values.update({'maritalStatus': maritalStatus})
                values.update({'gender': request.params['gender']})
                values.update({'sejelNo': request.params['sejelNo']})
                values.update({'sejel_place': request.params['sejel_place']})

                values.update({'id_no': request.params['id_no']})
                values.update({'stati_no': request.params['stati_no']})
                values.update({'registered_with': request.params['registered_with']})

                nationality = request.params['nationality']
                if nationality == '':
                    nationality = None

                values.update({'nationality': nationality})

                qatarfirstvisit_date = request.params['qatarfirstvisit_date']
                qatarfirstvisit = {}
                if qatarfirstvisit_date == '':
                    qatarfirstvisit_date = None
                qatarfirstvisit = {'qatarfirstvisit_date': datetime.strptime(qatarfirstvisit_date,
                                                                             '%d/%m/%Y') if qatarfirstvisit_date else None}
                values.update(qatarfirstvisit)

                values.update({'function': request.params['function']})

                values.update({'father_fullname': request.params['father_fullname']})
                values.update({'father_fullname_en': request.params['father_fullname_en']})

                values.update({'father_place_of_birth': request.params['father_place_of_birth']})

                father_date_of_birth = request.params['father_date_of_birth']
                father_date = {}

                if father_date_of_birth == '':
                    father_date_of_birth = None
                father_date = {'father_date_of_birth': datetime.strptime(father_date_of_birth,
                                                                         '%d/%m/%Y') if father_date_of_birth else None}
                values.update(father_date)

                father_religion = request.params['father_religion']
                if father_religion == '':
                    father_religion = None
                values.update({'father_religion': father_religion})
                values.update({'father_file_no': request.params['father_file_no']})
                values.update({'file_no': request.params['file_no']})

                values.update({'father_stati_no': request.params['father_stati_no']})
                values.update({'father_registered_with': request.params['father_registered_with']})
                values.update({'mother_place_of_birth': request.params['mother_place_of_birth']})

                mother_date_of_birth = request.params['mother_date_of_birth']
                mother_date = {}
                if mother_date_of_birth == '':
                    mother_date_of_birth = None
                mother_date = {'mother_date_of_birth': datetime.strptime(mother_date_of_birth,
                                                                         '%d/%m/%Y') if mother_date_of_birth else None}
                values.update(mother_date)
                print("-------mother date------", mother_date)
                religion = request.params['religion']
                if religion == '':
                    religion = None
                values.update({'religion': religion})

                mother_religion = request.params['mother_religion']
                if mother_religion == '':
                    mother_religion = None
                values.update({'mother_religion': mother_religion})
                values.update({'mother_file_no': request.params['mother_file_no']})
                values.update({'mother_stati_no': request.params['mother_stati_no']})
                values.update({'mother_registered_with': request.params['mother_registered_with']})

                partner.sudo().write(values)
                return request.make_response(json.dumps({
                    'status': "success",
                    'data': {'msg': _('Successfully Saved')}
                }), headers=headers)

        redirect = "/my/account"
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'tab': tab,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
        print("endingggggggggggggggggggggggggggggggggggggggggggggg", values)
        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route(['/my/account/insert_dependant'], type='http', auth='user', website=True)
    def contact_insert_dependant(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id

        sec_nationality = request.params['depsec_natio']
        if sec_nationality == '':
            sec_nationality = None
        country_id = request.params['depnationality']
        if country_id == '':
            country_id = 126

        dependent_type = request.params['dependent_type']
        if dependent_type == '':
            dependent_type = 'child'
        depfirstName = request.params['depfirstName']
        depmiddleName = request.params['depmiddleName']
        deplastName = request.params['deplastName']

        depfirstName_EN = request.params['depfirstName_EN']
        depmiddleName_EN = request.params['depmiddleName_EN']
        deplastName_EN = request.params['deplastName_EN']

        depdate = request.params['depdate']
        if depdate == '':
            depdate = None
        depplaceOfBirth = request.params['depplaceOfBirth']
        if depplaceOfBirth == '':
            depplaceOfBirth = None
        schoolName = request.params['schoolName']
        depmotherFullName = request.params['depmotherFullName']
        depmotherFullName_en = request.params['depmotherFullName_en']

        depfather_fullname = request.params['depfather_fullname']
        depnationality = request.params['depnationality']
        if depnationality == '':
            depnationality = None
        marriage_date = request.params['depmarriage_date']
        if marriage_date == '':
            marriage_date = None
        marriage_place = request.params['depmarriage_place']
        depcompany = request.params['depcompany']
        depphone = request.params['depphone']

        depfunction = request.params['depfunction']
        depCompanyAdd = request.params['depCompanyAdd']
        depkazaBirth = request.params['depkazaBirth']

        depsejelNo = None
        if post.__contains__('depsejelNo'):
            depsejelNo = request.params['depsejelNo']

        dep_file_no = None
        if post.__contains__('dep_file_no'):
            dep_file_no = request.params['dep_file_no']

        dep_stati_no = None
        if post.__contains__('dep_stati_no'):
            dep_stati_no = request.params['dep_stati_no']

        first_Nationality = partner.first_Nationality
        vals = {
            'name': depfirstName + ' ' + depmiddleName + ' ' + deplastName,
            'firstName': depfirstName,
            'middleName': depmiddleName,
            'lastName': deplastName,
            'first_name_en': depfirstName_EN,
            'middle_name_en': depmiddleName_EN,
            'last_name_en': deplastName_EN,
            'dependent_type': dependent_type,
            'person_type': 'child',
            'parent_id': partner.id,
            'sejelNo': depsejelNo,
            'function': depfunction,
            'marriage_place': marriage_place,
            'marriage_date': datetime.strptime(marriage_date, '%d/%m/%Y') if marriage_date else None,
            'schoolName': schoolName,
            'motherFullName': depmotherFullName,
            'mother_full_name_en': depmotherFullName_en,
            'file_no': dep_file_no,
            'stati_no': dep_stati_no,
            'placeOfBirth': depplaceOfBirth,
            'phone': depphone,
            'date': datetime.strptime(depdate, '%d/%m/%Y') if depdate else None,
            'father_fullname': depfather_fullname,
            'kazaBirth': depkazaBirth,
            'company_name': depcompany,
            'street': depCompanyAdd,
            'first_Nationality': first_Nationality
        }
        request.env['res.partner'].sudo().create(vals)

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"
                     }
        }), headers=headers)

    @http.route(['/my/account/insert_documents'], type='http', auth='user', website=True)
    def contact_insert_document(self, **post):
        partner = request.env.user.partner_id
        partner_doc_Id = request.params['partner_doc_Id']

        if post.__contains__('document_type'):
            document_type = request.params['document_type']

        docNo = request.params['docNo']
        issueDate = request.params['issueDate']
        if issueDate == '':
            issueDate = None;
        expiryDate = request.params['expiryDate']
        if expiryDate == '':
            expiryDate = None;
        folder = request.env['documents.folder'].search([('is_default_folder', '=', True)], limit=1)
        file = request.params['files[]']
        if file is not None and file is not '':
            attachment_64 = request.env['ir.attachment'].create({
                'name': file.filename,
                'datas': base64.b64encode(file.read()),
                'type': 'binary',
            })
        if partner_doc_Id is not None and partner_doc_Id is not '':
            document = request.env['documents.document'].search([('id', '=', partner_doc_Id)])
            if file is not None:
                document.write({'attachment_id': attachment_64.id,
                                'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
            else:
                document.write({'document_number': docNo,
                                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None})
        else:
            vals = {
                'type': 'binary',
                'document_type_id': document_type,
                'document_number': docNo,
                'issue_date': datetime.strptime(issueDate, '%d/%m/%Y') if issueDate else None,
                'expiry_date': datetime.strptime(expiryDate, '%d/%m/%Y') if expiryDate else None,
                'attachment_id': attachment_64.id,
                'partner_id': partner.id,
                'folder_id': folder.id,

            }
            request.env['documents.document'].create(vals)

        redirect = "/my/account/documents"
        if redirect:
            return request.redirect(redirect)

    @http.route(['/my/account/document_type'], type='http', auth='user', website=True)
    def get_documents_type(self):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        document_type_id = request.params['document_type']
        service_id = request.params['service_id']
        print(service_id)
        if not document_type_id:
            document_type_id = request.params['doctype']

        document_type = request.env['ebs_mod.document.types'].search([('id', '=', document_type_id)])

        return request.make_response(json.dumps({
            'status': "success",
            'data': {
                'is_required_issue_date': document_type.is_required_issue_date,
                'service_id': service_id,
                'is_required_expiry_date': document_type.is_required_expiry_date,
                'is_required_doc_no': document_type.is_required_doc_no,
            }
        }), headers=headers)

    @http.route(['/my/account/document/open/<int:id>'], type='http', auth='user', website=True)
    def documents_open(self, id):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        document = request.env['documents.document'].search([('id', '=', id)])

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'documentId': document.id,
                     'doctype': document.document_type_id.id,
                     'document_number': document.document_number,
                     'name': document.name,
                     'is_required_issue_date': document.document_type_id.is_required_issue_date,
                     'is_required_expiry_date': document.document_type_id.is_required_expiry_date,
                     'is_required_doc_no': document.document_type_id.is_required_doc_no,
                     # ,  'issue_date': document.issue_date,
                     #     'expiry_date': document.expiry_date,

                     }
        }), headers=headers)

    @http.route(['/my/account/insert_emergency'], type='http', auth='user', website=True)
    def contact_insert_emergency(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id

        emergency_full_name = request.params['emergency_full_name']
        emergency_phone_number = request.params['emergency_phone_number']
        emergency_full_name_leb = request.params['emergency_full_name_leb']
        emergency_phone_number_leb = request.params['emergency_phone_number_leb']

        previous = request.env['ebs_mod.contact.emergency'].search([('partner_id', '=', partner.id)])

        for em in previous:
            em.is_active = False

        request.env['ebs_mod.contact.emergency'].create({
            'emergency_full_name': emergency_full_name,
            'emergency_phone_number': emergency_phone_number,
            'emergency_full_name_leb': emergency_full_name_leb,
            'emergency_phone_number_leb': emergency_phone_number_leb,
            'is_active': True,
            'partner_id': partner.id
        })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/insert_ikama'], type='http', auth='user', website=True)
    def contact_insert_ikama(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id

        ikama_no = request.params['ikama_no']
        ikama_issue_date = request.params['ikama_issue_date']
        ikama_enddate = request.params['ikama_enddate']
        family_member = request.params['family_member']
        guarantor = request.params['guarantor']
        occupation = request.params['occupation']
        dependent = request.params['dependent']
        if dependent == '':
            dependent = None
        previous = request.env['ebs_mod.contact.ikama'].search([('partner_id', '=', partner.id)
                                                                   , ('family_member', '=', family_member)])
        for em in previous:
            em.is_active = False

        # objdate = datetime.strptime(ikama_issue_date, DEFAULT_SERVER_DATETIME_FORMAT)
        # print("-------------------date--------------",objdate)
        # ndate = objdate.strftime('%Y/%m/%d')
        # print("--------nndate-----",ndate)
        # nn = datetime.strptime(ndate, "%Y/%m/%d")
        # print("-------------------newdate--------nn------", nn,nn.date())
        # print("-------------------newdate--------------", type(nn))
        vals = {
            'ikama_enddate': datetime.strptime(ikama_enddate, '%d/%m/%Y') if ikama_enddate else None,
            'ikama_issue_date': datetime.strptime(ikama_issue_date, '%d/%m/%Y') if ikama_issue_date else None,
            'ikama_no': ikama_no,
            'dependent': dependent,
            'guarantor': guarantor,
            'occupation': occupation,
            'is_active': True,
            'partner_id': partner.id,
            'family_member': family_member
        }
        request.env['ebs_mod.contact.ikama'].create(vals)
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/insert_passports'], type='http', auth='user', website=True)
    def contact_insert_passport(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        travel_doc_type = request.params['travel_doc_type']
        passport_no = request.params['passport_no']
        passport_place = request.params['passport_place']
        passport_start_date = request.params['passport_start_date']
        if passport_start_date == '':
            passport_start_date = None
        passport_exp_date = request.params['passport_exp_date']
        if passport_exp_date == '':
            passport_exp_date = None
        family_member = request.params['family_member']
        dependent = request.params['dependent']
        if dependent == '':
            dependent = None
        previous = request.env['ebs_mod.contact.passport'].search([('partner_id', '=', partner.id)
                                                                      , ('family_member', '=', family_member)])

        for em in previous:
            em.is_active = False
        vals = {
            'passport_no': passport_no,
            'travel_doc_type': travel_doc_type,
            'passport_place': passport_place,
            'passport_start_date': datetime.strptime(passport_start_date, '%d/%m/%Y') if passport_start_date else None,
            'passport_exp_date': datetime.strptime(passport_exp_date, '%d/%m/%Y') if passport_exp_date else None,
            'is_active': True,
            'partner_id': partner.id,
            'family_member': family_member,
            'dependent': dependent
        }
        request.env['ebs_mod.contact.passport'].create(vals)

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/insert_company'], type='http', auth='user', website=True)
    def contact_insert_company(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        previous = request.env['ebs_mod.contact.address'].search([('partner_id', '=', partner.id)
                                                                     , ('type', '=', 'Company')])
        for em in previous:
            em.is_active = False
        start_date = request.params['address_start']
        if start_date == '':
            start_date = None

        partner_comp_Id = request.params['partner_comp_Id']
        if partner_comp_Id is not None and partner_comp_Id is not '':
            address = request.env['ebs_mod.contact.address'].search([('id', '=', partner_comp_Id)])
            address.write({'company_name': request.params['company_name'],
                           'street': request.params['street'],
                           'city': request.params['city'],
                           'phoneNumber': request.params['phoneNumber'],
                           'job_position': request.params['job_position'],
                           'pobox': request.params['pobox'],
                           'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None,
                           'is_active': True
                           })
        else:
            request.env['ebs_mod.contact.address'].create({
                'partner_id': partner.id,
                'type': 'Company',
                'company_name': request.params['company_name'],
                'street': request.params['street'],
                'city': request.params['city'],
                'phoneNumber': request.params['phoneNumber'],
                'job_position': request.params['job_position'],
                'pobox': request.params['pobox'],
                'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None,
                'is_active': True
            })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/insert_qatar'], type='http', auth='user', website=True)
    def contact_insert_qatar(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        previous = request.env['ebs_mod.contact.address'].search([('partner_id', '=', partner.id)
                                                                     , ('type', '=', 'Qatar')])
        for em in previous:
            em.is_active = False

        start_date = request.params['address_start']
        if start_date == '':
            start_date = None

        partner_qatar_Id = request.params['partner_qatar_Id']
        if partner_qatar_Id is not None and partner_qatar_Id is not '':
            address = request.env['ebs_mod.contact.address'].search([('id', '=', partner_qatar_Id)])
            address.write({'street': request.params['street'],
                           'qatar_region': request.params['qatar_region'],
                           'phoneNumber': request.params['phoneNumber'],
                           'building': request.params['building'],
                           'floor': request.params['floor'],
                           'flat': request.params['flat'],
                           'mojama3': request.params['mojama3'],
                           'mobile': request.params['mobile'],
                           'city': request.params['city'],
                           'pobox': request.params['pobox'],
                           'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None
                           })
        else:
            request.env['ebs_mod.contact.address'].create({
                'partner_id': partner.id,
                'type': 'Qatar',
                'street': request.params['street'],
                'qatar_region': request.params['qatar_region'],
                'phoneNumber': request.params['phoneNumber'],
                'building': request.params['building'],
                'floor': request.params['floor'],
                'flat': request.params['flat'],
                'mojama3': request.params['mojama3'],
                'mobile': request.params['mobile'],
                'city': request.params['city'],
                'pobox': request.params['pobox'],
                'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None,
                'is_active': True
            })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/insert_enroll'], type='http', auth='public', website=True, csrf=False)
    def contact_insert_enroll(self, **post):
        headers = [('Content-Type', 'application/json')]
        address_ids = [int(id) for id in request.params['enroll_addresses'].split(',')] if request.params['enroll_addresses'] else []
        social_media_ids = [int(id) for id in request.params['enroll_social_media_list'].split(',')] if request.params['enroll_social_media_list'] else []
        if post.get('create'):
            vals = {
                'name': request.params['enroll_name'],
                'type': 'new',
                'contact_type': post.get('contact_type_check_box'),
                'phone': request.params['enroll_phone'],
                'email': request.params['enroll_email'],
                'address_ids': [(6, 0, address_ids)],
                'social_media_ids': [(6, 0, social_media_ids)],
                'identification': base64.b64encode(post.get('identification').read()) if post.get(
                    'identification') else False
            }
            if post.get('contact_type_check_box') == 'company':
                vals.update({
                    'cr_number': request.params['enroll_cr_number'],
                    'industry_id': request.params['enroll_industry'],
                    'website': request.params['enroll_website'],
                    'authorization_letter': base64.b64encode(post.get('authorization_letter').read()) if post.get(
                        'authorization_letter') else False,
                    'copy_of_crp': base64.b64encode(post.get('copy_of_crp').read()) if post.get(
                        'copy_of_crp') else False,
                })
            else:
                vals.update({
                    'job_position': int(post.get('profile_job')) if post.get('profile_job') else False,
                    'permission_letter': base64.b64encode(post.get('permission_letter').read()) if post.get(
                        'permission_letter') else False,
                })
            request.env['ebs.enroll.requests'].create(vals)
        if post.get('update'):
            request.env['ebs.enroll.requests'].create({
                'name': request.params['enroll_name'],
                'type': 'update',
                'contact_type': 'company',
                'partner_id': int(post.get('enroll_id')),
                'cr_number': request.params['enroll_cr_number'],
                'industry_id': request.params['enroll_industry'],
                'phone': request.params['enroll_phone'],
                'email': request.params['enroll_email'],
                'website': request.params['enroll_website'],
                'address_ids': [(6, 0, address_ids)],
                'social_media_ids': [(6, 0, social_media_ids)],
            })
        return request.redirect('/')

    @http.route(['/my/account/delete_enroll'], type='http', auth='user', website=True)
    def delete_enrolled_company(self, **post):
        headers = [('Content-Type', 'application/json')]
        
        enrolled_company_id = request.env['res.partner'].sudo().browse(int(post.get('delete_enroll_id')))

        request.env['ebs.enroll.requests'].create({
            'name': enrolled_company_id.name,
            'type': 'delete',
            'contact_type': 'company',
            'partner_id': enrolled_company_id.id
        })

        return request.redirect('/my/account')

    @http.route(['/my/account/delete_enroll_request/<int:request_id>'], type='http', auth='user', website=True, csrf=False)
    def delete_enroll_request(self, request_id, **post):
        headers = [('Content-Type', 'application/json')]
        status = ''
        enrolled_request_id = request.env['ebs.enroll.requests'].sudo().browse(int(request_id))
        if enrolled_request_id.status == 'submitted':
            enrolled_request_id.sudo().unlink()
            status = 'success'
        return request.make_response(json.dumps({'status': status}), headers=headers)

    @http.route(['/my/account/insert_enroll_address'], type='http', auth='public', website=True, csrf=False)
    def insert_enroll_address(self, **post):
        headers = [('Content-Type', 'application/json')]

        enroll_address_id = request.env['ebs_mod.contact.address'].sudo().create({
            'type': post.get('address_type'),
            'street': post.get('address_street'),
            'city': post.get('address_city'),
            'pobox': post.get('address_pin'),
            'phoneNumber': post.get('address_phone'),
            'mobile': post.get('address_mobile'),
        })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': [enroll_address_id.id],
                     'type': post.get('address_type'),
                     'street': post.get('address_street'),
                     'city': post.get('address_city'),
                     'pobox': post.get('address_pin'),
                     'phoneNumber': post.get('address_phone'),
                     'mobile': post.get('address_mobile'),
                     }
        }), headers=headers)

    @http.route('/delete_address', type='json', auth='public', website='True')
    def delete_address(self, id, enroll_addresses, **kw):
        address_id = request.env['ebs_mod.contact.address'].sudo().browse(int(id))
        enroll_addresses = enroll_addresses.split(',')
        enroll_addresses.remove(id)
        address_id.sudo().unlink()
        return {'enroll_addresses': ','.join(enroll_addresses)}

    @http.route(['/my/account/insert_enroll_social_media'], type='http', auth='public', website=True, csrf=False)
    def insert_enroll_social_media(self, **post):
        headers = [('Content-Type', 'application/json')]
        type_id = request.env['ebs.socialmedia.types'].sudo().browse(int(post.get('social_media_type')))

        enroll_social_media_id = request.env['ebs.partner.socialmedia'].sudo().create({
            'type_id': type_id.id,
            'name': post.get('social_media_name'),
        })
        

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': [enroll_social_media_id.id],
                     'type': type_id.name,
                     'name': post.get('social_media_name'),
                     }
        }), headers=headers)

    @http.route('/delete_social_media', type='json', auth='public', website='True')
    def delete_social_media(self, id, enroll_social_media_list, **kw):
        social_media_id = request.env['ebs_mod.contact.address'].sudo().browse(int(id))
        enroll_social_media_list = enroll_social_media_list.split(',')
        enroll_social_media_list.remove(id)
        social_media_id.sudo().unlink()
        return {'enroll_social_media_list': ','.join(enroll_social_media_list)}

    @http.route(['/my/account/insert_lebanon'], type='http', auth='user', website=True)
    def contact_insert_lebanon(self, **post):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        previous = request.env['ebs_mod.contact.address'].search([('partner_id', '=', partner.id)
                                                                     , ('type', '=', 'Lebanon')])
        for em in previous:
            em.is_active = False

        owned = True
        # owned = False
        #
        # if post.__contains__('owned'):
        #     if request.params['owned'] == 'on':
        #         owned = True

        start_date = request.params['address_start']
        if start_date == '':
            start_date = None
        partner_leb_Id = request.params['partner_leb_Id']
        if partner_leb_Id is not None and partner_leb_Id is not '':
            address = request.env['ebs_mod.contact.address'].search([('id', '=', partner_leb_Id)])
            address.write({'street': request.params['street'],
                           'region': request.params['region'],
                           'phoneNumber': request.params['phoneNumber'],
                           'building': request.params['building'],
                           'floor': request.params['floor'],
                           'flat': request.params['flat'],
                           'city': request.params['city'],
                           'kaza': request.params['kaza'],
                           'town': request.params['town'],
                           'district': request.params['district'],
                           'mobile': request.params['mobile'],
                           'owned': owned,
                           'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None,
                           'is_active': True
                           })
        else:
            request.env['ebs_mod.contact.address'].create({
                'partner_id': partner.id,
                'type': 'Lebanon',
                'street': request.params['street'],
                'region': request.params['region'],
                'phoneNumber': request.params['phoneNumber'],
                'building': request.params['building'],
                'floor': request.params['floor'],
                'flat': request.params['flat'],
                'city': request.params['city'],
                'kaza': request.params['kaza'],
                'town': request.params['town'],
                'district': request.params['district'],
                'mobile': request.params['mobile'],
                'owned': owned,
                'address_start': datetime.strptime(start_date, '%d/%m/%Y') if start_date else None,
                'is_active': True
            })

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'status': "success"}
        }), headers=headers)

    @http.route(['/my/account/qatar/open/<int:id>'], type='http', auth='user', website=True)
    def qatar_open(self, id):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        address = request.env['ebs_mod.contact.address'].search([('id', '=', id)])

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': address.id,
                     'city': address.city,
                     'street': address.street,
                     'qatar_region': address.qatar_region,
                     'building': address.building,
                     'floor': address.floor,
                     'mojama3': address.mojama3,
                     'flat': address.flat,
                     'phoneNumber': address.phoneNumber,
                     'mobile': address.mobile,
                     'pobox': address.pobox

                     }
        }), headers=headers)
            
    @http.route(['/my/account/enroll/open/<int:id>'], type='http', auth='user', website=True)
    def enroll_open(self, id):
        headers = [('Content-Type', 'application/json')]
        enroll = request.env['res.partner'].search([('id', '=', id)])

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': enroll.id,
                     'name': enroll.name,
                     'cr_number': enroll.cr_number or '',
                     'industry': enroll.industry_id.id or '',
                     'phone': enroll.phone or '',
                     'email': enroll.email or '',
                     'website': enroll.website or '',
                     }
        }), headers=headers)

    @http.route(['/my/account/company/open/<int:id>'], type='http', auth='user', website=True)
    def company_open(self, id):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        address = request.env['ebs_mod.contact.address'].search([('id', '=', id)])
        print(
            address
        )
        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': address.id,
                     'company_name': address.company_name,
                     'street': address.street,
                     'city': address.city,
                     'phoneNumber': address.phoneNumber,
                     'job_position': address.job_position,
                     'pobox': address.pobox
                     }
        }), headers=headers)

    @http.route(['/my/account/lebanon/open/<int:id>'], type='http', auth='user', website=True)
    def lebanon_open(self, id):
        headers = [('Content-Type', 'application/json')]
        partner = request.env.user.partner_id
        address = request.env['ebs_mod.contact.address'].search([('id', '=', id)])

        return request.make_response(json.dumps({
            'status': "success",
            'data': {'id': address.id,
                     'region': address.region.id,
                     'kaza': address.kaza.id,
                     'town': address.town,
                     'city': address.city,
                     'street': address.street,
                     'district': address.district,
                     'building': address.building,
                     'floor': address.floor,
                     'flat': address.flat,
                     'mobile': address.mobile,
                     'phoneNumber': address.phoneNumber,
                     'owned': address.owned
                     }
        }), headers=headers)

    @http.route(['/show_profile'], type='http', auth='user', website=True, csrf=False)
    def show_profile_request(self, **post):
        headers = [('Content-Type', 'application/json')]
        request.env['ebs.enroll.requests'].sudo().create({
            'name': request.env.user.partner_id.name,
            'partner_id': request.env.user.partner_id.id,
            'type': 'show',
            'contact_type': 'person',
            'job_position': int(post.get('profile_job')) if post.get('profile_job') else False,
            'permission_letter': base64.b64encode(post.get('permission_letter').read()),
        })
        return request.redirect('/my/account')

    @http.route(['/hide_profile'], type='http', auth='user', website=True, csrf=False)
    def hide_profile_request(self, **post):
        headers = [('Content-Type', 'application/json')]
        request.env['ebs.enroll.requests'].sudo().create({
            'name': request.env.user.partner_id.name,
            'partner_id': request.env.user.partner_id.id,
            'type': 'hide',
            'contact_type': 'person',
        })
        return request.redirect('/my/account')

    @http.route('/enroll', type='http', auth='public', website='True')
    def enroll_page(self):
        values = self._prepare_portal_layout_values()
        return http.request.render('ebs_qsheild_mod.enroll_webpage', values)
