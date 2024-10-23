odoo.define('ebs_qsheild_mod.portal', [], function (require){
'use strict';
    var core = require('web.core');
    var ajax = require('web.ajax');
//    var _t = core._t;
    var _t = require('@web/core/l10n/translation');
    console.log("....................")
    $(document).ready(function(){

        var curday = function(sp){
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //As January is 0.
        var yyyy = today.getFullYear();

        if(dd<10) dd='0'+dd;
        if(mm<10) mm='0'+mm;
        return (dd+sp+mm+sp+yyyy);
        };
        $('#portal_report_form_dateofapploication').val(curday('/'))
    });
     $(document).on('change','#nationalityspouse_data_report', function(){
        var nationality_spouse = $('#nationalityspouse_data_report').children("option:selected").val()
        if(nationality_spouse == 'other'){
            console.log("..................other.........")
           $('.other_nationality_second_div').show();
           $('.other_nationality_first_div').hide();
        }
        else{
            console.log("..................else.........")
            $('.other_nationality_second_div').hide();
            $('.other_nationality_first_div').hide();
        }
    });

    $(document).on('keypress','#portal_report_form_qid_no', function(ev){
         console.log(ev.which)
//        ev.preventDefault();
        ev.stopPropagation();
        var list = [48,49,50,51,52,53,54,55,56,57,32]
        if (list.includes(ev.which)){
            console.log("saaaaaaaaaaaa")
            return true
        }
        else{
            alert("please insert number value!")
            return false
        }

    });
    $(document).on('keypress','#portal_report_form_mobile', function(ev){
         console.log(ev.which)
//        ev.preventDefault();
        ev.stopPropagation();
        var list = [48,49,50,51,52,53,54,55,56,57,32]
        if (list.includes(ev.which)){
            console.log("saaaaaaaaaaaa")
            return true
        }
        else{
            alert("please insert number value !")
            return false
        }

    });
    $(document).on('keypress','#portal_report_form_moblileno', function(ev){
         console.log(ev.which)
//        ev.preventDefault();
        ev.stopPropagation();
        var list = [48,49,50,51,52,53,54,55,56,57,32]
        if (list.includes(ev.which)){
            console.log("saaaaaaaaaaaa")
            return true
        }
        else{
            alert("please insert number value !")
            return false
        }

    });

    $(document).on('keypress','#portal_report_form_mobilenoqatar', function(ev){
         console.log(ev.which)
//        ev.preventDefault();
        ev.stopPropagation();
        var list = [48,49,50,51,52,53,54,55,56,57,32]
        if (list.includes(ev.which)){
            console.log("saaaaaaaaaaaa")
            return true
        }
        else{
            alert("please insert number value !")
            return false
        }

    });

    $(document).on('keypress','#portal_report_form_emergencycontact', function(ev){
             console.log(ev.which)
    //        ev.preventDefault();
            ev.stopPropagation();
            var list = [48,49,50,51,52,53,54,55,56,57,32]
            if (list.includes(ev.which)){
                return true
            }
            else{
                alert("please insert number value!")
                return false
            }

        });
        $(document).on('keypress','#portal_report_form_fax', function(ev){
             console.log(ev.which)
    //        ev.preventDefault();
            ev.stopPropagation();
            var list = [48,49,50,51,52,53,54,55,56,57,32]
            if (list.includes(ev.which)){
                return true
            }
            else{
                alert("please insert number value!")
                return false
            }

        });


    $(document).on('click','#save_data_report_form', function(){
        var archive_no = $('#poratl_report_form_archive_number').val()
        var portal_service_request_id = $("#portal_service_request_id").val()
        var portal_service_request_id_new = $("#portal_service_request_id_new").val()
        var portal_service_request_spouse_id = $("#portal_service_request_spouse_id").val()
        var person_name = $('#portal_report_form_person_name').val()
        var Nationality = $("#nationality_form_report_id").children("option:selected").val()
        var qid = $("#portal_report_form_qid_no").val()
        var spouse_name = $("#partner_data_report").val()
        var nationality_of_spouse = $("#nationalityspouse_data_report").children("option:selected").val()
        var other_nationality = $(".other_nationality").val()
        var sponsor_name = $("#portal_report_form_sponsor_name").val()
        var sponsor_mobile = $("#portal_report_form_mobile").val()
        var leb_description = $("#portal_report_form_streetlabanon_description").val()
        var qtr_description = $("#portal_report_form_streetqatar_description").val()
        var sponsor_fax = $("#portal_report_form_fax").val()
        var pobox = $("#portal_report_form_pobox").val()
        var education = $("#portal_report_form_education").val()
        var school_university = $("#portal_report_form_schooluniversituname").val()
        var certificateissue_date = $("#certificateissue_date").val()
        var labnon_street = $("#portal_report_form_streetlabanon").val()
        var labnon_owned = $("#owned_form_report_id").val()
        var labnon_mobile = $("#portal_report_form_moblileno").val()
        var labnon_floor = $("#portal_report_form_floorno").val()

        var qatar_street = $("#portal_report_form_streetqatar").val()
        var qatar_buliding = $("#portal_report_form_buildingqatar").val()
        var qatar_mobile = $("#portal_report_form_mobilenoqatar").val()
        var qatar_floor = $("#portal_report_form_floornoqatar").val()
        var emergency_name = $("#portal_report_form_emergencyname").val()
        var emergency_contact = $("#portal_report_form_emergencycontact").val()
        var portal_report_date = $("#portal_report_form_dateofapploication").val()
        console.log("...leb_description...",leb_description)
        console.log("...qtr_description...",qtr_description)
//        if(qid  )
//            console.log(event.which ascii('0'))
//        if (event.ctrlKey && event.which == ascii("0")
        if(person_name != '' &&  Nationality != '' &&  qid != '' &&  sponsor_name != '' &&  education != '' &&  school_university != '' &&  certificateissue_date != '' &&  labnon_street != '' &&  labnon_owned != '' &&  labnon_mobile != '' &&  labnon_floor != '' &&  qatar_street != '' &&  qatar_buliding != '' &&  qatar_mobile != '' &&  qatar_floor != '' && emergency_name != '' && emergency_contact != '' && portal_report_date != '' && leb_description != '' && qtr_description != ''){
            ajax.jsonRpc('/portal/report/data/print/','call',{
                'service_request_id':portal_service_request_id,
                'qtr_description':qtr_description,
                'leb_description':leb_description,
                'service_request_id_new':portal_service_request_id_new,
                'portal_service_request_spouse_id':portal_service_request_spouse_id,
                'archive_no':archive_no,
                'other_nationality':other_nationality,
                'person_name':person_name,
                'Nationality':Nationality,
                'qid':qid,
                'spouse_name':spouse_name,
                'nationality_of_spouse':nationality_of_spouse,
                'sponsor_name':sponsor_name,
                'sponsor_mobile':sponsor_mobile,
                'sponsor_fax':sponsor_fax,
                'pobox':pobox,
                'education':education,
                'school_university':school_university,
                'certificateissue_date':certificateissue_date,
                'labnon_street':labnon_street,
                'labnon_owned':labnon_owned,
                'labnon_mobile':labnon_mobile,
                'labnon_floor':labnon_floor,
                'qatar_street':qatar_street,
                'qatar_buliding':qatar_buliding,
                'qatar_mobile':qatar_mobile,
                'qatar_floor':qatar_floor,
                'emergency_name':emergency_name,
                'emergency_contact':emergency_contact,
                'portal_report_date':portal_report_date,
            }).then(function(data){
                console.log("..data..",data)
                 $('#print_data_report_form').attr('href','/web/content/'+parseInt(data)+'?download=true');
                 $('#print_data_report_form').show();
            });
        }
        else{
            alert("please fill-up all informations !")
        }
    });
    jQuery( document ).ready(function() {

        if($('#status').val() != 'progress'){
            $('.success_alert').hide();
        }
        else{
            $(".success_alert").show("slow").delay(3000).hide("slow");
        }
        $('.close').show();
        $('.image_click').click(function(ev){
            console.log("clicked",$(this).siblings('.type_id').val());
            ajax.jsonRpc("/my/service/insert_form",'call',{'service':$(this).siblings('.type_id').val()}).then(function (data) {
                console.log(data);
                $(location).attr('href','/my/'+$('.service_name').val()+'/insert_doc_form/'+data['id']);
            });

        });
        var $star_rating = $('.star-rating .fa');
        $star_rating.on('click', function() {
//            console.log("@@@@@@@@@@@@",$(this).data('rating'),$(this).data('comments'));
//            ajax.jsonRpc("/my/service/submit_feedback",'call',{'rating':$(this).data('rating'),'comments':$(this).data('comments')}).then(function (data) {
//                console.log(data);
//                $(location).attr('href','/my/'+$('.service_name').val()+'/insert_doc_form/'+data['id']);
//            });
            $star_rating.siblings('input.rating-value').val($(this).data('rating'));
            return $star_rating.each(function() {
                if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
                  return $(this).removeClass('fa-star-o').addClass('fa-star');
                } else {
                  return $(this).removeClass('fa-star').addClass('fa-star-o');
                }
            });

        });

        $('#submit_btn').click(function(event){
                if($('#type').val() == 'auth'){
                      var url='/my/authorization/submit_authorization';
                        var formValues=  $('#authorization_form').serialize();
                        $.post(url, formValues, function(data)
                        {
//                            $(location).attr('href','/my/authorization/insert_doc_form/'+data.data.id);
                        });

                }
                if($('#type').val() == 'passport'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#passports_form').serialize();

                    $.post(url, formValues, function(data)
                    {
                        /*$(location).attr('href','/my/passports/insert_doc_form/'+data.data.id);*/
                    });
                }
                if($('#type').val() == 'personal'){
                        console.log('-------------------------------------------------------');
                        var url='/my/authorization/submit_authorization';
                        var formValues=  $('#personal_form').serialize();
                        var valid = validateForm();
                        $.post(url, formValues, function(data)
                        {
        //                                $(location).attr('href','/my/personal/insert_doc_form/'+data.data.id);
                        });
                    }
                if($('#type').val() == 'visa'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#visa_form').serialize();

                    $.post(url, formValues, function(data)
                    {
//                        $(location).attr('href','/my/ta2shirat/insert_doc_form/'+data.data.id);

                     });
                }
                if($('#type').val() == 'ifadat'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#ifadat_form').serialize();
                    $.post(url, formValues, function(data)
                    {
//                        $(location).attr('href','/my/ifadat/insert_doc_form/'+data.data.id);
                     });
                }
                if($('#type').val() == 'tasdikat'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#tasdikat_form').serialize();
                    $.post(url, formValues, function(data)
                    {
                        $('.success_alert').show();
//                        $(location).attr('href','/my/tasdikat/insert_doc_form/'+data.data.id);
                     });

                }

        });

        $('.close').click(function(event)
        {
            location.reload();
        });

        $("#save-feedback-btn").click(function(event)
        {

            var url='/my/service/submit_feedback';
            var formValues=  $('#feedback_form').serialize();
             var comments=$('#feedback_form').find("[name='comments']").val()
            if (comments == ''){
                alert("please enter Comment")
            }
            else{
            $.post(url, formValues, function(data)
            {
                $('.loader_for_service_submit').addClass('fa fa-spinner fa-spin');
                location.reload();
/*                if($('#type').val() == 'auth'){
                      var url='/my/authorization/submit_authorization';
                        var formValues=  $('#authorization_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(location).attr('href','/my/authorization/insert_doc_form/'+data.data.id);
                        });

                }
                if($('#type').val() == 'passport'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#passports_form').serialize();

                    $.post(url, formValues, function(data)
                    {
                        $(location).attr('href','/my/passports/insert_doc_form/'+data.data.id);
                    });
                }
                if($('#type').val() == 'personal'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#personal_form').serialize();
                    var valid = validateForm();
//                      if(valid)
//                      {
                            $.post(url, formValues, function(data)
                            {
                                $(location).attr('href','/my/personal/insert_doc_form/'+data.data.id);
                            });
//                      }
//                      else
//                      {
//                            window.scrollTo(500, 500);
//                      }
                }
                if($('#type').val() == 'visa'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#visa_form').serialize();

                    $.post(url, formValues, function(data)
                    {
                        $(location).attr('href','/my/ta2shirat/insert_doc_form/'+data.data.id);

                     });
                }
                if($('#type').val() == 'ifadat'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#ifadat_form').serialize();
                    $.post(url, formValues, function(data)
                    {
                        $(location).attr('href','/my/ifadat/insert_doc_form/'+data.data.id);
                     });
                }
                if($('#type').val() == 'tasdikat'){
                    var url='/my/authorization/submit_authorization';
                    var formValues=  $('#tasdikat_form').serialize();
                    $.post(url, formValues, function(data)
                    {
                        $('.success_alert').show();
                        $(location).attr('href','/my/tasdikat/insert_doc_form/'+data.data.id);
                     });

                }*/

            });
            }
        });

    });
    console.log("/././././././././././")

    $(document).on('click','.applicant_job_history', function(){
        $('body').addClass('applicant_data_class');
    })
    $(document).on('click','.applicant_educational_info', function(){
        $('body').removeClass('applicant_data_class');
    })

    $(document).on('click','#create_new_rec_line_education_info', function(ev){
    console.log("...............................click.......")
    if(ev.target.dataset.id){
        var degree = $('#education_degree_new_rec_amount').val()
        var year_from = $('#education_year_from_new_rec_amount').val()
        var year_to = $('#education_year_to_new_rec_amount').val()
        var subject = $('#education_subject_new_rec_amount').val()
        var major = $('#education_major_new_rec').val()
        var country = $('#education_country_id').children("option:selected").val()
        ajax.jsonRpc('/applicant/education/info/','call',{
        'degree':degree,
        'year_from':year_from,
        'year_to':year_to,
        'subject':subject,
        'major':major,
        'country':country,
         }).then(function(){
            location.reload();
         });
    }
    else{
        var name =  $('#job_applicant_name').val()
        var contact_email = $('#job_applicant_email').val()
        var family_name = $('#job_applicant_family_name').val()
        var contact_phone = $('#job_applicant_phone_no').val()
        var date_of_birth = $('#job_applicant__date_of_birth').val()
        var notice_period = $('#job_applicant_notice_period').children("option:selected").val()
        var pass_no = $('#job_applicant__passport_no').val()
        var marital_status = $('#job_applicant_marital_status').children("option:selected").val()
        var pass_issu_place = $('#job_applicant__passport_issuance_place').val()
        var add_qatar = $('#job_applicant_address_qatar').val()
        var pass_issu_date = $('#job_applicant__passport_issuance_date').val()
        var cv_summary = $('#job_applicant_cv_summary').val()
        var pass_expiry_date = $('#job_applicant__passport_expiry_date').val()
        var skills = $('#job_applicant_skills').val()
        var resident_in_qatar = $('#job_applicant_resident_in_qatar').children("option:selected").val()
        if(resident_in_qatar == 'no'){
            var qid = ''
        }
        if(resident_in_qatar == 'yes'){
            var qid = $('#job_applicant_qid').val()
        }

        var qid_expiry_date = $('#job_applicant_qid_expiry_date').val()
        var cover_letter = $('#job_applicant_cover_letter').val()
        var degree = $('#education_degree_new_rec_amount').val()
        var year_from = $('#education_year_from_new_rec_amount').val()
        var year_to = $('#education_year_to_new_rec_amount').val()
        var subject = $('#education_subject_new_rec_amount').val()
        var major = $('#education_major_new_rec').val()
        var country = $('#education_country_id').children("option:selected").val()
        var cover_letter = $('#job_applicant_cover_letter')[0].files[0];
        var cv_attachment = $('#job_applicant_cv_attachment')[0].files[0];
        if(name && contact_email && family_name && contact_phone && date_of_birth && notice_period && pass_no && marital_status && pass_issu_place
        && add_qatar && pass_issu_date && cv_summary && pass_expiry_date && skills && resident_in_qatar && qid && qid_expiry_date && cover_letter && cv_attachment){
         var reader = new FileReader();
         var reader1 = new FileReader();
        console.log("........................iffffffffffffff")
        reader.readAsDataURL(cover_letter)
        reader1.readAsDataURL(cv_attachment)
        reader.onload = function(e){
            window.sessionStorage.setItem('cover_letter_data', e.target.result);
        }
        reader1.onload = function(e){
            window.sessionStorage.setItem('cv_attachment_data', e.target.result);
        }
        ajax.jsonRpc('/applicant/education/info/','call',{
        'degree':degree,
        'year_from':year_from,
        'year_to':year_to,
        'subject':subject,
        'major':major,
        'country':country,
         'name':name,
         'contact_email':contact_email,
         'family_name':family_name,
         'contact_phone':contact_phone,
         'date_of_birth':date_of_birth,
         'notice_period':notice_period,
         'pass_no':pass_no,
         'marital_status':marital_status,
         'pass_issu_place':pass_issu_place,
         'add_qatar':add_qatar,
         'pass_issu_date':pass_issu_date,
         'cv_summary':cv_summary,
         'pass_expiry_date':pass_expiry_date,
         'skills':skills,
         'resident_in_qatar':resident_in_qatar,
         'qid':qid,
         'qid_expiry_date':qid_expiry_date,
         'cover_letter':window.sessionStorage.getItem('cover_letter_data'),
         'cv_attachment':window.sessionStorage.getItem('cv_attachment_data'),
         }).then(function(){
            location.reload();
         });
    }
    else{
            alert("Please Insert All Applicant's Data !")
         }
    }


//         };
//         }
    });

    $(document).on('click','#create_new_rec_line_job_history', function(ev){
    console.log("...............................click.......",ev.target.id)
    console.log("...............................click.......",ev)
    if(ev.target.dataset.id){
        var position = $('#job_history_position_new_rec').val()
        var company_name = $('#job_company_name_new_rec').val()
        var start_date = $('#job_starting_date_new_rec').val()
        var end_date = $('#job_end_date_new_rec').val()
        var description  = $('#job_description_new_rec').val()
        var country = $('#job_history_country_id').children("option:selected").val()
        var current_position = $('#job_current_position').children("option:selected").val()
        ajax.jsonRpc('/applicant/job/history/info/','call',{
        'position':position,
        'company_name':company_name,
        'start_date':start_date,
        'end_date':end_date,
        'description':description,
        'country':country,
        'current_position':current_position,

         }).then(function(){
            location.reload();
         });
    }
    else{

    var name =  $('#job_applicant_name').val()
    var contact_email = $('#job_applicant_email').val()
    var family_name = $('#job_applicant_family_name').val()
    var contact_phone = $('#job_applicant_phone_no').val()
    var date_of_birth = $('#job_applicant__date_of_birth').val()
    var notice_period = $('#job_applicant_notice_period').children("option:selected").val()
    var pass_no = $('#job_applicant__passport_no').val()
    var marital_status = $('#job_applicant_marital_status').children("option:selected").val()
    var pass_issu_place = $('#job_applicant__passport_issuance_place').val()
    var add_qatar = $('#job_applicant_address_qatar').val()
    var pass_issu_date = $('#job_applicant__passport_issuance_date').val()
    var cv_summary = $('#job_applicant_cv_summary').val()
    var pass_expiry_date = $('#job_applicant__passport_expiry_date').val()
    var skills = $('#job_applicant_skills').val()
    var resident_in_qatar = $('#job_applicant_resident_in_qatar').children("option:selected").val()
    if(resident_in_qatar == 'no'){
        var qid = ''
    }
    if(resident_in_qatar == 'yes'){
        var qid = $('#job_applicant_qid').val()
    }
//    var qid = $('#job_applicant_qid').val()
    var qid_expiry_date = $('#job_applicant_qid_expiry_date').val()
    var cover_letter = $('#job_applicant_cover_letter').val()
    var position = $('#job_history_position_new_rec').val()
    var company_name = $('#job_company_name_new_rec').val()
    var start_date = $('#job_starting_date_new_rec').val()
    var end_date = $('#job_end_date_new_rec').val()
    var description  = $('#job_description_new_rec').val()
    var country = $('#job_history_country_id').children("option:selected").val()
    var current_position = $('#job_current_position').children("option:selected").val()
    console.log("..........$('#job_applicant_cover_letter')...",$('#job_applicant_cover_letter'))
    if($('#job_applicant_cover_letter')[0] && $('#job_applicant_cv_attachment')[0]){
        var cover_letter = $('#job_applicant_cover_letter')[0].files[0];
        var cv_attachment = $('#job_applicant_cv_attachment')[0].files[0];
    }


    if(name && contact_email && family_name && contact_phone && date_of_birth && notice_period && pass_no && marital_status && pass_issu_place
    && add_qatar && pass_issu_date && cv_summary && pass_expiry_date && skills && resident_in_qatar && qid && qid_expiry_date && cover_letter && cv_attachment){
         var reader = new FileReader();
         var reader1 = new FileReader();
        console.log("........................iffffffffffffff")
        reader.readAsDataURL(cover_letter)
        reader1.readAsDataURL(cv_attachment)
        reader.onload = function(e){
            window.sessionStorage.setItem('cover_letter_data', e.target.result);
        }
        reader1.onload = function(e){
            window.sessionStorage.setItem('cv_attachment_data', e.target.result);
        }
        ajax.jsonRpc('/applicant/job/history/info/','call',{
        'position':position,
        'company_name':company_name,
        'start_date':start_date,
        'end_date':end_date,
        'description':description,
        'country':country,
        'current_position':current_position,
         'name':name,
         'contact_email':contact_email,
         'family_name':family_name,
         'contact_phone':contact_phone,
         'date_of_birth':date_of_birth,
         'notice_period':notice_period,
         'pass_no':pass_no,
         'marital_status':marital_status,
         'pass_issu_place':pass_issu_place,
         'add_qatar':add_qatar,
         'pass_issu_date':pass_issu_date,
         'cv_summary':cv_summary,
         'pass_expiry_date':pass_expiry_date,
         'skills':skills,
         'resident_in_qatar':resident_in_qatar,
         'qid':qid,
         'qid_expiry_date':qid_expiry_date,
         'cover_letter':window.sessionStorage.getItem('cover_letter_data'),
         'cv_attachment':window.sessionStorage.getItem('cv_attachment_data'),
         }).then(function(){
            location.reload();
         });
    }
    else{
            alert("Please Insert All Applicant's Data !")
         }
    }
    });


    $(document).on('click','#edit_create_new_rec_line_education_info', function(ev){
    console.log("...............................click.......")
        var education_rec_id = ev.target.dataset.id
        var degree = $('#edit_education_degree_new_rec').val()
        var year_from = $('#edit_education_year_from_new_rec').val()
        var year_to = $('#edit_education_year_to_new_rec').val()
        var subject = $('#edit_education_subject_new_rec').val()
        var major = $('#edit_education_major_new_rec').val()
        var country = $('#edit_education_country_id').children("option:selected").val()
        ajax.jsonRpc('/applicant/edit/education/info/','call',{
        'degree':degree,
        'year_from':year_from,
        'year_to':year_to,
        'subject':subject,
        'major':major,
        'country':country,
        'education_rec_id':education_rec_id
         }).then(function(){
            $('#edit_education_new_rec_line_close').click()
            location.reload();

         });


    });

    $(document).on('click','#edit_create_new_rec_line_job_history', function(ev){
    console.log("...............................click.......")
        var job_rec_id = ev.target.dataset.id
        var position = $('#edit_job_position_new_rec').val()
        var start_date = $('#edit_job_strt_date_to_new_rec').val()
        var end_date = $('#edit_job_end_date_new_rec').val()
        var description = $('#edit_job_description_new_rec').val()
        var company_name = $('#edit_job_company_name_new_rec').val()
        var country = $('#edit_job_history_country_id').children("option:selected").val()
        var current_position = $('#edit_job_history_current_position').children("option:selected").val()
        ajax.jsonRpc('/applicant/edit/job/history/','call',{
        'position':position,
        'start_date':start_date,
        'end_date':end_date,
        'description':description,
        'company_name':company_name,
        'country':country,
        'current_position':current_position,
        'job_rec_id':job_rec_id
         }).then(function(){
            $('#edit_job_history_rec_line_close').click()
            location.reload();
         });



});

$(document).on('click','.save_job_data', function(ev){
    console.log("...............................click.......")
        var job_vac_id = $('#job_vacancies_rec_id').val()
        var job_applicant_id = $('#job_vacancies_hidden_applicant_id').val()
        if(job_applicant_id){
            ajax.jsonRpc('/vacancies/save/job/','call',{
            'job_vac_id':job_vac_id,
            'job_applicant_id':job_applicant_id,
             }).then(function(data){
             if(data == false){
                alert("This job has been Already Applied!")
             }
             else{
                location.reload();
                alert("This job has been saved successfully!")

            }
             });
             }
         else{
            alert("Please make first Your Profile!")
         }


    });

    $(document).on('click','#create_new_point_of_contact', function(ev){
    console.log("...............................click.......",ev.target.id)
    console.log("...............................click.......",ev)
    if(ev.target.dataset.id){
        var company_rec = ev.target.dataset.id
        var name = $('#company_new_name_id').val()
        var position = $('#company_new_job_position_id').val()
        var email = $('#company_new_email_id').val()
        var phone = $('#company_new_phone_id').val()
        ajax.jsonRpc('/company/point/of/contact/line/','call',{
        'company_rec':company_rec,
        'name':name,
        'position':position,
        'email':email,
        'phone':phone,
         }).then(function(){
            location.reload();
         });
    }
    else{

        var company_name =  $('#job_company_name').val()
        var industry_id = $('#job_company_industry_id').children("option:selected").val()
        var number_of_employees = $('#job_number_of_employees_id').children("option:selected").val()
        var name = $('#company_new_name_id').val()
        var position = $('#company_new_job_position_id').val()
        var email = $('#company_new_email_id').val()
        var phone = $('#company_new_phone_id').val()

        if(name && number_of_employees){
            ajax.jsonRpc('/company/point/of/contact/line/','call',{
            'company_name':company_name,
            'industry_id':industry_id,
            'number_of_employees':number_of_employees,
            'name':name,
            'position':position,
            'email':email,
            'phone':phone,
             }).then(function(){
                location.reload();
             });
        }
    else{
            alert("Please Insert All Company's Data !")
         }
    }
    });

    $(document).on('click','#edit_company_point_of_contact_save', function(ev){
    console.log("...............................click.......")
        var company_point_of_contact_id = ev.target.dataset.id
        var name = $('#edit_company_point_of_contact_name').val()
        var position = $('#edit_company_job_position_id').val()
        var email = $('#edit_job_company_email_id').val()
        var phone = $('#edit_company_phone_id').val()
        ajax.jsonRpc('/company/edit/point/of/contact/','call',{
            'name':name,
            'position':position,
            'email':email,
            'phone':phone,
            'company_point_of_contact_id':company_point_of_contact_id
         }).then(function(){
            $('#edit_company_point_of_contact_close').click()
            location.reload();
         });
    });
    $(document).on('click','.seekers_save_job_data', function(ev){
        var seekers_job_vacancies_applicant_rec_id = ev.target.dataset.id
        ajax.jsonRpc('/vacancies/applicant/seekers/record/','call',{
            'seekers_job_vacancies_applicant_rec_id':seekers_job_vacancies_applicant_rec_id,
         }).then(function(data){
            if(data == false){
            alert("This profile has been Already Saved!")
         }
         else{
            location.reload();
            alert("Profile is saved successfully!")
        }
         });
    });

        $(document).on('click','#create_new_vacancies_record_id', function(ev){
        console.log("...............................click.......",$('#create_vacancies_publishing_date').val())
            var position_name = $('#create_vacancies_position_name').val()
            var publising_date = $('#create_vacancies_publishing_date').val()
            var description = $('#create_job_vacancies_description').val()
            var educational_requirement = $('#create_job_vacancies_eductional_requirement').val()
            var skills_requirement = $('#create_job_vacancies_skills_requirement').val()
            var joining_limit = $('#create_job_joining_limit').val()
            var benefits = $('#create_job_vacancies_benefits').val()
            var expiry_date = $('#create_job_vacancy_expire_date').val()
            var application_link = $('#create_job_vacancies_application_link').val()
            var application_mail = $('#create_job_vacancies_application_email').val()
            var work_location = $('#create_job_vacancies_work_location').val()
            console.log("publising_date....joining_limit......expiry_date..",publising_date,joining_limit,expiry_date)
            if(position_name && publising_date && description && educational_requirement && skills_requirement && joining_limit && benefits && expiry_date && application_link && application_mail && work_location){
                ajax.jsonRpc('/company/job/vacancies/create/','call',{
                    'position_name':position_name,
                    'publising_date':publising_date,
                    'description':description,
                    'educational_requirement':educational_requirement,
                    'skills_requirement':skills_requirement,
                    'benefits':benefits,
                    'joining_limit':joining_limit,
                    'expiry_date':expiry_date,
                    'application_link':application_link,
                    'application_mail':application_mail,
                    'work_location':work_location,
                 }).then(function(){
                    $('#create_new_vacancies_close').click()
                    location.reload();
                 });
                 }
                 else{
                    alert("Please insert vacancies Data!")
                 }

    });

     $(document).on('change','#filter_vacanices_record', function(ev){
        console.log("...............................click.......")
        var search_input = $('#filter_vacanices_record').val()
        ajax.jsonRpc('/search/vacancies/record','call',{
            'search_input':search_input,
         }).then(function(data){
         console.log("..1....data......",data)
         if(data){
         console.log("...2...data......",data)
            window.location.href= "/job/vacancies/record?search=" + data
            console.log("........window.location.href......",window.location.href)
         }

         });



});

 $(document).on('change','#filter_jobseekers_record', function(ev){
        console.log("...............................click.......")
        var search_input = $('#filter_jobseekers_record').val()
        var search_input_resident = $('#filter_resident_in_qatar_record').children("option:selected").val()
        console.log("search_input.....search_input_resident.................",search_input,search_input_resident)
        ajax.jsonRpc('/search/jobseekers/record','call',{
         'search_input':search_input,
         'search_input_resident':search_input_resident,
         }).then(function(data){
            console.log("..1....data......",data)
         if(data.search){
            window.location.href= "/company/job/seekers?search=" + data.search
         }
         if(data.resident_in_qatar){
            window.location.href= "/company/job/seekers?search=" + data.resident_in_qatar
         }
        if(data.resident_in_qatar && data.search){
            window.location.href= "/company/job/seekers?search=" + data.search + "&resident_in_qatar=" + data.resident_in_qatar
         }
        });
});

$(document).on('change','#filter_resident_in_qatar_record', function(ev){
        console.log("................ccccccclllc...............click.......")
        var search_input = $('#filter_jobseekers_record').val()
        var search_input_resident = $('#filter_resident_in_qatar_record').children("option:selected").val()
        console.log("search_input.....search_input_resident.................",search_input,search_input_resident)
        ajax.jsonRpc('/search/jobseekers/resident/record','call',{
         'search_input':search_input,
         'search_input_resident':search_input_resident,
         }).then(function(data){
            console.log("......data......",data)
         if(data.search){
         console.log("..............data.search/......",data.search)
            window.location.href= "/company/job/seekers/?search=" + data.search
         }
         if(data.resident_in_qatar){
         console.log("..............data.resident_in_qatar/......",data.resident_in_qatar)
            window.location.href= "/company/job/seekers/?resident_in_qatar=" + data.resident_in_qatar
         }
        if(data.resident_in_qatar && data.search){
            window.location.href= "/company/job/seekers/?search=" + data.search + "&resident_in_qatar=" + data.resident_in_qatar
         }
        });



});

    $(document).ready(function(ev){
    var resident_in_qatar = $('#job_applicant_resident_in_qatar').children("option:selected").val()

        if(resident_in_qatar == 'no'){
            $('.applicant_qid_number_div').hide()
        }
    });
    $(document).on('change','#job_applicant_resident_in_qatar', function(ev){
       var resident_in_qatar = $('#job_applicant_resident_in_qatar').children("option:selected").val()
        if(resident_in_qatar == 'no'){
            $('.applicant_qid_number_div').hide()
        }
        else{
            $('.applicant_qid_number_div').show()
        }




});


    $(document).on('click','#recruitments_radio_button', function(ev){
        $('body').addClass('recruitment_show_class');
    });

    $(document).on('click','#electronic_radio_button', function(ev){
      $('body').removeClass('recruitment_show_class');
    });


    $(document).on('click','.education_info_remove_class', function(ev){
    console.log("...............................click.......")
        var education_info_line_id = ev.target.dataset.id
        ajax.jsonRpc('/education/line/remove/','call',{
            'education_info_line_id':education_info_line_id,
         }).then(function(){
            location.reload();
         });
    });

    $(document).on('click','.point_of_remove_line', function(ev){
    console.log("...............................click.......")
        var point_of_remove_line = ev.target.dataset.id
        ajax.jsonRpc('/point/of/contact/line/remove/','call',{
            'point_of_remove_line':point_of_remove_line,
         }).then(function(){
            location.reload();
         });
    });

    $(document).on('click','.job_history_remove_line_class', function(ev){
    console.log("...............................click.......")
        var job_history_line_id = ev.target.dataset.id
        ajax.jsonRpc('/job/history/line/remove','call',{
            'job_history_line_id':job_history_line_id,
         }).then(function(){
            location.reload();
         });
    });

    $(document).on('change','#filter_individual_contact_record', function(ev){
        var search_input = $('#filter_individual_contact_record').val()
        ajax.jsonRpc('search/individual_contacts','call',{
            'search_input':search_input,
        }).then(function(data){
            if(data){
                window.location.href= "/individual_contacts?search=" + data
            }
        });
    });

    $(document).on('change','#filter_company_contact_record', function(ev){
        var search_input = $('#filter_company_contact_record').val()
        ajax.jsonRpc('search/company_contacts','call',{
            'search_input':search_input,
        }).then(function(data){
            if(data){
                window.location.href= "/company_contacts?search=" + data
            }
        });
    });

    $(document).on('click','.delete_address', function(ev){
        var address_id = ev.currentTarget.dataset.value
        var enroll_id = ev.currentTarget.dataset.enroll
        var modal = ''
        if (enroll_id) {
            modal = '#openenrollModal_' + enroll_id
        }
        else {
            modal = '#enroll_page_form'
        }
        ajax.jsonRpc('/delete_address','call',{
            'id':address_id,
            'enroll_addresses': $(modal + ' #enroll_addresses').val()
        }).then(function(data){
            $(modal + ' #enroll_addresses').val(data.enroll_addresses);
            $(modal + ' #address_' + address_id).remove();
        });
    });

    $(document).on('click','.delete_social_media', function(ev){
        var social_media_id = ev.currentTarget.dataset.value
        var modal = '#enroll_page_form'
        ajax.jsonRpc('/delete_social_media','call',{
            'id':social_media_id,
            'enroll_social_media_list': $(modal + ' #enroll_social_media_list').val()
        }).then(function(data){
            $(modal + ' #enroll_social_media_list').val(data.enroll_social_media_list);
            $(modal + ' #social_media_' + social_media_id).remove();
        });
    });

    $(document).on('click','.delete_enroll', function(ev){
        var enroll_id = ev.currentTarget.dataset.value
        $(".modal-body #delete_enroll_id").val(enroll_id);
        $('#deleteEnrollModal').modal('toggle');
    });

    $(document).on('click','.open_enroll_modal', function(ev){
        var enroll_id = ev.currentTarget.dataset.value
        $('#openenrollModal_' + enroll_id).modal('toggle');
    });

    $(document).on('click','.add_address', function(ev){
        $("#address_type").val('Lebanon');
        $("#address_street").val('');
        $("#address_city").val('');
        $("#address_pin").val('');
        $("#address_phone").val('');
        $("#address_mobile").val('');
        if (ev.currentTarget.dataset.enroll) {
            $("#address_enroll_id").val(ev.currentTarget.dataset.enroll);
        }
        else {
            $("#enroll_page").val(true);
        }
        $('#addressModal').modal('toggle');
    });

    $(document).on('click','.add_social_media', function(ev){
        $("#social_media_type").val('');
        $("#social_media_name").val('');
        $('#socialmediaModal').modal('toggle');
    });

    $(document).on('click','.add_enroll_address', function(ev){
        debugger;
        var url='/my/account/insert_enroll_address';
        var enroll_id = $('#add_address_form #address_enroll_id').val()
        var modal = ''
        if (enroll_id) {
            modal = '#openenrollModal_' + enroll_id
        }
        if ($("#enroll_page").val()) {
            modal = '#enroll_page_form'
        }
        var formValues= $('#add_address_form').serialize();
        $.post(url, formValues, function(data) {
            if(data.status == 'success'){
                var row = '<tr id="address_' + data.data.id + '"><td>' + data.data.type + '</td><td>' + data.data.street + '</td><td>' + data.data.city + '</td><td>' + data.data.pobox + '</td><td>' + data.data.phoneNumber + '</td><td>' + data.data.mobile + '</td><td><i class="fa fa-trash delete_address" style="cursor: pointer;" data-value="' + data.data.id + '" data-enroll="' + enroll_id + '"/></td></tr>'
                $(modal + ' #enroll_address_table tr:last').after(row);
                var enroll_addresses = $(modal + ' #enroll_addresses').val();
                if (enroll_addresses == "") {
                    $(modal + ' #enroll_addresses').val(data.data.id);
                }
                else {
                    $(modal + ' #enroll_addresses').val(enroll_addresses.concat(",", data.data.id));
                }
            }
        });
    });

    $(document).on('click','.add_enroll_social_media', function(ev){
        debugger;
        var url='/my/account/insert_enroll_social_media';
        var modal = '#enroll_page_form'
        var formValues= $('#add_social_media_form').serialize();
        $.post(url, formValues, function(data) {
            if(data.status == 'success'){
                var row = '<tr id="social_media_' + data.data.id + '"><td>' + data.data.type + '</td><td>' + data.data.name + '</td><td><i class="fa fa-trash delete_social_media" style="cursor: pointer;" data-value="' + data.data.id + '"/></td></tr>'
                $(modal + ' #enroll_social_media_table tr:last').after(row);
                var enroll_social_media_list = $(modal + ' #enroll_social_media_list').val();
                if (enroll_social_media_list == "") {
                    $(modal + ' #enroll_social_media_list').val(data.data.id);
                }
                else {
                    $(modal + ' #enroll_social_media_list').val(enroll_social_media_list.concat(",", data.data.id));
                }
            }
        });
    });

    $(document).on('click','#display_profile', function(ev){
        $('#showProfileModal').modal('toggle');
    });

    $(document).on('click','#hide_profile', function(ev){
        $('#hideProfileModal').modal('toggle');
    });

    $(document).on('change','#profile_job', function(ev){
        if ($(ev.currentTarget).children("option:selected").data() && $(ev.currentTarget).children("option:selected").data().attachment){
            $('#permission_letter').toggleClass('required');
            $('#permission_letter').attr('required', true);
            $('#permission_letter_container').removeClass('d-none');
        }
        else {
            $('#permission_letter').toggleClass('required');
            $('#permission_letter').attr('required', false);
            $('#permission_letter_container').addClass('d-none');
        }
    });

    $(document).on('click','#contact_type_company', function(ev){
        $('.company_fields').removeClass('d-none');
        $('.individual_fields').addClass('d-none');
        $('#enroll_cr_number').attr('required', true);
        $('#authorization_letter').attr('required', true);
        $('#copy_of_crp').attr('required', true);
        $('#profile_job').attr('required', false);
        $('#permission_letter_container').addClass('d-none');
        $('#permission_letter').attr('required', false);
    });

    $(document).on('click','#contact_type_individual', function(ev){
        $('.company_fields').addClass('d-none');
        $('.individual_fields').removeClass('d-none');
        $('#profile_job').attr('required', true);
        if ($('#profile_job').children("option:selected").data() && $('#profile_job').children("option:selected").data().attachment){
            $('#permission_letter').attr('required', true);
            $('#permission_letter_container').removeClass('d-none');
        }
        else {
            $('#permission_letter').attr('required', false);
            $('#permission_letter_container').addClass('d-none');
        }
        $('#enroll_cr_number').attr('required', false);
        $('#authorization_letter').attr('required', false);
        $('#copy_of_crp').attr('required', false);
    });

});


