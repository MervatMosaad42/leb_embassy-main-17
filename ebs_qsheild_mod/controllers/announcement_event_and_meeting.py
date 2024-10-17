from odoo import http
from odoo.http import request

class Announcement(http.Controller):
    @http.route('/announcement', type='http', auth='public',website='True')
    def announcement(self):
        announcement_data = request.env['circulars.page'].search([('page_active','=',True)])
        return http.request.render('ebs_qsheild_mod.announcement_template', {"announcement_data":announcement_data})

    @http.route(['/my/statement/<model("circulars.page"):circular>'], type='http', auth="user", website=True)
    def partner_statement(self, **kwargs):
        circular = kwargs.get('circular')
        bytes = circular.attachment_field
        print("...........bytes........",type(bytes))
        reporthttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(bytes)),
        ]
        print(".........reporthttpheaders...",reporthttpheaders)
        return request.make_response(bytes, headers=reporthttpheaders)

class AmbassadorActivitiesMeetings(http.Controller):
    @http.route('/ambassador_activities_and_meetings', type='http', auth='public',website='True')
    def ambassador_activities_meetings(self):
        meetings_data = request.env['meetings.meetings'].search([('page_active','=',True)])
        return http.request.render('ebs_qsheild_mod.ambassador_activities_meetings_template', {'meetings_data':meetings_data})


    @http.route('/events_and_meetings', type='http', auth='public',website='True')
    def events_and_meetings(self):
        return http.request.render('ebs_qsheild_mod.events_and_meetings_template', {})

class EmbassyEventsActivities(http.Controller):
    @http.route('/embassy_events_and_activities', type='http', auth='public',website='True')
    def embassy_events_activities(self):
        events_activities_data = request.env['events_activities.events_activities'].search([('page_active','=',True)])
        return http.request.render('ebs_qsheild_mod.embassy_events_and_activities_template', {'events_activities_data':events_activities_data})

class AnnouncementData(http.Controller):
    @http.route(['/announcement/<model("circulars.page"):circular>'], auth='public', website="True")
    def circular_data(self, **kw):
        circular = kw.get('circular')
        return http.request.render('ebs_qsheild_mod.circular_page_template', {
            'circular_data':circular,
        })

class AmbassadorActivitiesMeetingsData(http.Controller):
    @http.route(['/ambassador_activities/<model("meetings.meetings"):meeting>'], auth='public', website="True")
    def ambassador_activities_meetings_data(self, **kw):
        meeting = kw.get('meeting')
        return http.request.render('ebs_qsheild_mod.meeting_page_template', {
            'meeting_page_data':meeting,
        })

class EmbassyEventsActivitiesData(http.Controller):
    @http.route(['/embassy_events_and_activities/<model("events_activities.events_activities"):embassy>'], auth='public', website="True")
    def ambassador_activities_meetings_data(self, **kw):
        embassy = kw.get('embassy')
        return http.request.render('ebs_qsheild_mod.embassy_events_and_activities__page_template', {
            'embassy_page_data':embassy,
        })

class FeedBack(http.Controller):
    @http.route('/feedback/', auth='public', type='http' , website="True")
    def feedback_method(self, **kw):
        print(".,,,,,,,,,,,,,,,call feedback,,,,,,,,,")
        feedback = kw.get('feedback')
        return http.request.render('ebs_qsheild_mod.ebs_feedback_template', {
            'feedback_data':feedback,
        })

    @http.route('/feedback_submit/', type='json' ,auth='public', website="True",methods=['POST'])
    def feedback_submit_method(self, **kw):
        print(".,,,,,,,,,,,,,,,feedback_submit,,,,,,,,,",kw)
        rating = '0'
        if kw.get('rating') == '1':
            rating = '1'
        if kw.get('rating') == '2':
            rating = '2'
        if kw.get('rating') == '3':
            rating = '3'
        if kw.get('rating') == '4':
            rating = '4'
        if kw.get('rating') == '5':
            rating = '5'
        if kw.get('name') and kw.get('comments'):
            request.env['feedback.feedback'].sudo().create({
                'name':kw.get('name'),
                'email':kw.get('email'),
                'description':kw.get('description'),
                'rating':rating,
                'comments':kw.get('comments')
            })
            return True
        else:
            return False


