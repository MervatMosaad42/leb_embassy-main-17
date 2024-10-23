odoo.define('ebs_qsheild_mod.website_feedback_form',[], function (require) {
'use strict';


    var ajax = require('web.ajax');
    var jsonrpc = require('@web/core/network/rpc_service')

    //        var dom = require('web.dom');
    //        var Dialog = require("web.Dialog");
    //        var Widget = require("web.Widget");

    var rpc = require("web.rpc");
    var href = window.location.href;

    $(document).ready(function(){


            $(".o_website_feedback_form_send").click(function(){

                    var name = $(".feedback_name_class")[0].value
                    if (name == ''){
                        alert("Please Enter Name !");
                    }
                    var description = $(".feedback_description_class")[0].value
                    var email = $(".feedback_email_class")[0].value
                    var comments = $(".feedback_comments_class")[0].value
                    var rating1 = $("#rating1")[0].checked;
                    var rating2 = $("#rating2")[0].checked;
                    var rating3 = $("#rating3")[0].checked;
                    var rating4 = $("#rating4")[0].checked;
                    var rating5 = $("#rating5")[0].checked;
                    if(rating1 == true){
                        var rating = $("#rating1")[0].value
                    }
                     if(rating2 == true){
                        var rating = $("#rating2")[0].value
                    }
                     if(rating3 == true){
                        var rating =  $("#rating3")[0].value
                    }
                     if(rating4 == true){
                           var rating = $("#rating4")[0].value
                        }
                     if(rating5 == true){
                        var rating =$("#rating5")[0].value
                    }


                    $.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: '/feedback_submit/',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {rating,email,description,name,comments}}),
                    success: function (data) {
                        if (data.result == true) {
                            $('.feedback_website_main_page').css('display','none');
                            $('#thank_you_feedback').css('display','block');
                        } else {
                            alert("Please Enter name and Comments !");
                        }
                    },
                });

                 });


                 $('.rating_class').click(function(){
                    console.log(".......aaaaaaaaaaa")
                        if ($(this)[0].value == '1'){
                            $('.feedback_comments_class')[0].value =("سيئ جدا");
                        }
                        if ($(this)[0].value == '2'){
                            $('.feedback_comments_class')[0].value=("سيء");
                        }
                        if ($(this)[0].value == '3'){
                            $('.feedback_comments_class')[0].value=("جيد");
                        }
                        if ($(this)[0].value == '4'){
                            $('.feedback_comments_class')[0].value=("جيد جدا");
                        }
                        if ($(this)[0].value == '5'){
                            $('.feedback_comments_class')[0].value=("ممتاز");
                        }
             });

            });

});