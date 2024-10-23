# -*- coding: utf-8 -*-
{
    'name': "QSheild Module",

    'summary': """
        This module contains custom modifications for QSsheild
        """,

    'description': """
       This module contains custom modifications for QSsheild
    """,

    'author': "Jaafar Khansa",
    'website': "http://www.ever-bs.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'utm',
        'contacts',
        'hr',
        'documents',
        'password_security',
        'website',
        'snailmail',
        'portal',
        'web',

    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/email_template.xml',
        'data/website_data.xml',
        'data/circular_event_activity_and_meeting_menu.xml',

        'wizards/create_contact_document_wiz.xml',
        'wizards/message_wiz_view.xml',
        'wizards/enroll_request_reject_view.xml',

        # 'static/src/xml/assets.xml',
        # 'views/documents_assets.xml',

        'cron/document_cron_job.xml',

        # 'views/footer_view.xml',
        'views/homepage.xml',

        'views/aboutembassy_template.xml',
        'views/contacts_view_custom.xml',
        'views/contracts_view.xml',
        'views/contact_address_view.xml',
        'views/feedback_view.xml',
        'views/contact_relation_type_view.xml',
        'views/document_custom.xml',
        'views/document_folder_custom.xml',
        'views/document_types_view.xml',
        'views/expense_types_view.xml',
        'views/service_types_view.xml',
        'views/service_request_view.xml',
        'views/tickets_view_custom.xml',
        'views/service_workflow_config_view.xml',
        'views/service_request_workflow_view.xml',
        'views/service_request_divorce_template.xml',
        'views/service_request_marriage_report_template.xml',
        'views/service_request_palestinian_documnet_template.xml',
        'views/service_request_lebanese_born_template.xml',
        'views/pal_document_template.xml',
        'views/Job_vacancies.xml',
        'views/contact_payment_view.xml',
        'views/service_expenses_view.xml',
        'views/contact_payment_transaction_view.xml',
        'views/setting_view.xml',
        'views/menus.xml',
        'views/contact_passport_view.xml',
        'views/contact_ikama_view.xml',
        'views/contact_emergency_view.xml',
        'views/country_regions_view.xml',
        'views/news_view.xml',
        'views/res_company_custom_view.xml',
        'views/website_info_view.xml',
        'views/circular_event_meeting_view.xml',
        'views/announcement_template.xml',
        'views/embassy_events_and_activities_template.xml',
        'views/ambassador_activities_and_meetings_template.xml',
        'views/events_and_meetings_template_view.xml',
        'views/website_feedback_view.xml',
        'views/website_feedback_page_template.xml',
        'views/ambassador_greetings_view.xml',
        'views/portal_report_template.xml',
        'views/ebs_partner_socialmedia_view.xml',
        'views/ebs_enroll_requests_view.xml',
        'views/he_job_view.xml',


        'portal/contact_info_portal.xml',
        'portal/contact_visa_portal.xml',
        'portal/contact_authorization_portal.xml',
        'portal/contact_passport_portal.xml',
        'portal/contact_personal_portal.xml',
        'portal/contact_mou3amalt_konsoliya_portal.xml',
        'portal/portal_templates.xml',
        'portal/job_vacancies_portal_view.xml',
        'portal/contact_details_templates.xml',
        'portal/portal_layout.xml',

        'report/report.xml',
        'report/report_passport_electronic.xml',
        'report/report_lebaneselejel_custom.xml',
        'report/report_lebaneselejel_custom2.xml',
        'report/report_palestinianSejel.xml',
        'report/report_passport_leb.xml',
        'report/report_passport_leb2.xml',
        'report/report_passport_pal.xml',
        'report/report_passport_pal2.xml',
    ],
    'assets': {
            'web.assets_frontend': [
                '/ebs_qsheild_mod/static/src/css/homepage.css',
                '/ebs_qsheild_mod/static/src/css/owl.carousel.css',
                '/ebs_qsheild_mod/static/src/css/Font_face/font_face.css',
                '/ebs_qsheild_mod/static/src/css/lightbox.css',
                '/ebs_qsheild_mod/static/src/css/marquee.scss',


                '/ebs_qsheild_mod/static/src/js/owl.carousel.js',
                '/ebs_qsheild_mod/static/src/js/portal.js',
                '/ebs_qsheild_mod/static/src/js/feedback_form.js',
                '/ebs_qsheild_mod/static/src/js/contact_info_portal_copy.js',
                '/ebs_qsheild_mod/static/src/js/homepage.js',


                '/ebs_qsheild_mod/static/src/js/lightbox.js',
                # '/ebs_qsheild_mod/static/src/js/documents_search_panel_copy.js',

            ],
            'web.report_assets_pdf': [
                '/ebs_qsheild_mod/static/src/css/Font_face/report_font.css',
            ],
    },

}
