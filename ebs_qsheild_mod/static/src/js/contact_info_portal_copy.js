odoo.define('ebs_qsheild_mod.contract_info_portal', [], function (require){
'use strict';
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = require('@web/core/l10n/translation');
    console.log('called!');


    $(document).on('click','#docBtn', function(ev){

        $('#docModal').modal('toggle');
    });

    $(document).on('click','#add_qatar', function(ev){

        $('#qatarModal').modal('toggle');
    });

    $(document).on('click','#myBtn', function(ev){

            $('#myModal').modal('toggle');
    });


    $(document).on('click','#add_lebanon', function(ev){

        $('#lebanonModal').modal('toggle');
    });



    $(document).on('click','#add_passport', function(ev){

            $('#passportsModal').modal('toggle');
    });


    $(document).on('click','#add_emergency', function(ev){

                $('#emergencyModal').modal('toggle');
    });


    $(document).on('click','#save-qatar-btn', function(ev){

        console.log('zft');
        var url='/my/account/insert_qatar';
        var formValues= $('#qatar_form').serialize();
        $.post(url, formValues, function(data)
           {
                if(data.data.status == 'success')
                {
                    $(location).attr('href','/my/account/qatar');
                }
           });
    });


    $(document).on('click','#save-leb-btn', function(ev){

        var url='/my/account/insert_qatar';
        var formValues= $('#qatar_form').serialize();
        $.post(url, formValues, function(data)
           {
                var url='/my/account/insert_lebanon';
                var formValues= $('#leb_form').serialize();
                $.post(url, formValues, function(data)
                {
                     if(data.data.status == 'success')
                     {
                          $(location).attr('href','/my/account/lebanon');
                     }
                });
           });
    });


    $(document).on('click','#save-dependant-btn', function(ev){

        var url='/my/account/insert_dependant';
        var formValues= $('#dep_form').serialize();
        $.post(url, formValues, function(data)
        {
             if(data.data.status == 'success')
             {
                  $(location).attr('href','/my/account/dependants');
             }
        });
    });


    $(document).on('click','#save-passports-btn', function(ev){

                    var url=' /my/account/insert_passports';
                    var formValues= $('#passport_form').serialize();
                    $.post(url, formValues, function(data)
                    {
                         if(data.data.status == 'success')
                         {
                              $(location).attr('href','/my/account/passports');
                         }
                            else{alert("Expiry Date is not set properly.")}
                    });
        });


    $(document).on('click','#save-emergency-btn', function(ev){
            var url='/my/account/insert_emergency';
            var formValues= $('#emergency_form').serialize();
            $.post(url, formValues, function(data)
            {
                 if(data.data.status == 'success')
                 {
                      $(location).attr('href','/my/account/emergency');
                 }
            });
    });

    $(document).on('click','#save-info-btn', function(ev){
                var url='/my/account';
                var formValues= $('#info_form').serialize();

                $.post(url, formValues, function(data){
                        if(data.status == "success")
                            window.scrollTo(0, 0);
                            $(location).attr('href','/my/account');
                   });
        });


    $(document).on('click','#submit-info-btn', function(ev){
            var url='/my/account/submit';
            var formValues = $('#info_form').serialize();

//            formValues['im_image'] = $('#profile-pic-upload').val()
            $.post(url, formValues, function(data)
            {
                console.log('zeroo', data.status)
               if(data.status == "success")
               {
                   window.scrollTo(0, 0);
                   $(location).attr('href','/my/home');
               }
               else
               {
                   window.scrollTo(0, 0);
                   $('#error_message_div').html("&lt;div  class='alert alert-danger' role='alert' >"+data.msg+"&lt;/div>");
               }

           });
    });



    function parseDMY(isDate)
        {
            console.log('parseDMY Function!!')
            auto_save();
            console.log("parse");
            tmp = isDate.value;
            if(tmp){
                tmp = tmp.split("-");
                refDate = tmp[1]+"/"+tmp[2]+"/"+tmp[0];
                if (!validate(refDate))
                {
                    isDate.value = "";
                    isDate.focus();
                }
            }
        }


    function save_image()
          {
            var url='/my/account/save_image';
            var formValues= $('#info_form').serialize();
            $.post(url, formValues, function(data){
               });
          }


 });