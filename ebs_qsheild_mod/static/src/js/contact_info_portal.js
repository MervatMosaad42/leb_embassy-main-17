odoo.define('ebs_qsheild_mod.contact_info_portal',[], function (require) {

    var ajax = require('web.ajax');
    var jsonrpc = require('@web/core/network/rpc_service');
    var rpc = require("web.rpc");

    $(document).ready(function()
    {

        function save_passports()
             {
                    console.log('mero test');
                    var url=' /my/account/insert_passports';
                    var formValues= $('#passport_form').serialize();

                    $.post(url, formValues, function(data)
                    {
                        if(data.data.status == 'success')
                        {
                            $(location).attr('href','/my/account/passports');
                        }
                        else
                        {
                            alert("Expiry Date is not set properly.")
                        }

                    });
                    }
                    function validate(isDate)
                    {
                        console.log("###");
                        isValid = true;
                        tmp = isDate.split("/");
                        isLeap = tmp[2]%4;
                        if (!/[1-9]{1}/.test(tmp[0]) || /[1-9]{2}/.test(tmp[0]) & !/10|11|12/.test(tmp[0]))
                            {isValid = false}
                        else if ((/4|6|9|11/.test(tmp[0])) & tmp[1] > 30)
                            {isValid=false}
                        else if ((/1|3|5|7|8|10|12/.test(tmp[0])) & tmp[1] > 31)
                            {isValid=false}
                        else if ((tmp[0] == 2 & isLeap == 0) & tmp[1] > 29)
                            {isValid = false}
                        else if ((tmp[0] == 2 & isLeap != 0) & tmp[1] > 28)
                            {isValid = false}
                        else if (tmp[2].length != 4 || (!/^19|20/.test(tmp[2])))
                            {isValid = false}
                        if (isNaN(Date.parse(isDate)) || !isValid)
                            {return true}
                        else
                            { return true }
                    }

                    function parseDMY(isDate)
                    {
                        auto_save();
                        console.log("parse");
                        tmp = isDate.value;
                        if(tmp)
                        {
                            tmp = tmp.split("-");
                            refDate = tmp[1]+"/"+tmp[2]+"/"+tmp[0];
                            if (!validate(refDate))
                                {
                                    isDate.value = "";
                                    isDate.focus();
                                }
                        }
                    }

                    $(function ()
                    {
                        var tab = $('#tab').val();
                        if(tab != '')
                        {
                            $('.nav-tabs a[href="#'+tab+'"]').addClass("active");
                            $("#"+tab).addClass("show active");
                            if(tab != 'qatar')
                            {
                                window.scrollTo(0,document.body.scrollHeight);
                            }
                        }
                        var nationality = $('#first_Nationality').val();
                        if(nationality == "leb")
                        {
                            $("#pal").hide();
                            $("#pal1").hide();
                            $("#pal2").hide();
                            $("#pal3").hide();
                            $("#country").hide();
                            $("#motherreligion").show();

                        }
                        else if ( nationality == "pal")
                        {
                            $("#motherreligion").hide();
                            $("#pal").show();
                            $("#pal1").show();
                            $("#pal2").show();
                            $("#pal3").show();
                            $("#leb").hide();
                            $("#kaza").hide();
                            $("#country").hide();
                        }
                        else
                        {
                            $("#pal").hide();
                            $("#pal1").hide();
                            $("#pal2").hide();
                            $("#pal3").hide();
                            $("#leb").hide();
                            $("#kaza").hide();
                            $("#country").show();
                            $("#motherreligion").hide();

                        }

                        var dependent_type = $('#dependent_type').val();
                        if(dependent_type == "spouse")
                        {
                            $("#depChild").hide();
                        }


                        var status = $('#status').val();
                        if(status == "progress" || status == "confirm")
                        {
                            $("#save-info-btn").hide();
                            $("#submit-info-btn").hide();
                            $("#first_Nationality").attr('disabled','disabled');
                            $("#firstName").attr('disabled','disabled');
                            $("#middleName").attr('disabled','disabled');
                            $("#lastName").attr('disabled','disabled');
                            $("#motherFullName").attr('disabled','disabled');
                            $("#kazaBirth").attr('disabled','disabled');
                            $("#placeOfBirth").attr('disabled','disabled');
                            $("#firstName_EN").attr('disabled','disabled');
                            $("#middleName_EN").attr('disabled','disabled');
                            $("#lastName_EN").attr('disabled','disabled');
                            $("#motherFullName_EN").attr('disabled','disabled');
                            $("#placeOfBirth_EN").attr('disabled','disabled');
                            $("#date_of_birth").attr('disabled','disabled');
                            $("#birth_certificate_nb").attr('disabled','disabled');
                            $("#birth_certificate_date").attr('disabled','disabled');
                            $("#maritalStatus").attr('disabled','disabled');
                            $("#gender").attr('disabled','disabled');
                            $("#sejelNo").attr('disabled','disabled');
                            $("#sejel_place").attr('disabled','disabled');
                            $("#id_no").attr('disabled','disabled');
                            $("#stati_no").attr('disabled','disabled');
                            $("#registered_with").attr('disabled','disabled');
                            $("#qatarfirstvisit_date").attr('disabled','disabled');
                            $("#function").attr('disabled','disabled');
                            $("#father_fullname").attr('disabled','disabled');
                            $("#father_fullname_en").attr('disabled','disabled');
                            $("#father_place_of_birth").attr('disabled','disabled');
                            $("#email").attr('disabled','disabled');
                            $("#nationality").attr('disabled','disabled');
                            $("#father_date_of_birth").attr('disabled','disabled');
                            $("#father_religion").attr('disabled','disabled');
                            $("#father_file_no").attr('disabled','disabled');
                            $("#father_stati_no").attr('disabled','disabled');
                            $("#father_registered_with").attr('disabled','disabled');
                            $("#mother_place_of_birth").attr('disabled','disabled');
                            $("#mother_date_of_birth").attr('disabled','disabled');
                            $("#father_place_of_birth").attr('disabled','disabled');
                            $("#mother_religion").attr('disabled','disabled');
                            $("#religion").attr('disabled','disabled');
                            $("#mother_file_no").attr('disabled','disabled');
                            $("#mother_stati_no").attr('disabled','disabled');
                            $("#mother_registered_with").attr('disabled','disabled');
                            $("#file_no").attr('disabled','disabled');
                            $("#country_id").attr('disabled','disabled');
                            $("#btn_new_record").hide();
                            $(".btn_new_record").hide();
                            $("#myBtn").show();
                            $("#docBtn").show();
                            $("#add_emergency").show();
                            $("#add_ikama").show();
                            $("#add_passport").show();
                            $("#add_company").show();
                            $("#add_qatar").show();
                            $("#add_lebanon").show();
                        }


                        var url='/my/account/document_type';
                        formValues = $('#doc_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(".modal-body #is_required_issue_date").prop( "checked", data.data.is_required_issue_date );
                            $(".modal-body #is_required_expiry_date").prop( "checked", data.data.is_required_expiry_date );
                            $(".modal-body #is_required_doc_no").prop( "checked", data.data.is_required_doc_no );
                            if(data.data.is_required_issue_date==true)
                            {
                                $(".modal-body #issueDatediv").show();
                                $("#issueDate").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #issueDatediv").hide();
                                $("#issueDate").removeAttr('required');
                            }

                            if(data.data.is_required_expiry_date==true)
                            {
                                $(".modal-body #expiryDatediv").show();
                                $("#expiryDate").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #expiryDatediv").hide();
                                $("#expiryDate").removeAttr('required');
                            }

                            if(data.data.is_required_doc_no==true)
                            {
                                $(".modal-body #docNodiv").show();
                                $("#docNo").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #docNodiv").hide();
                                $("#docNo").removeAttr('required');
                            }

                        });
                    });


                    $('#document_type').on('change',function()
                    {
                        var url='/my/account/document_type';
                        formValues = $('#doc_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(".modal-body #is_required_issue_date").prop( "checked", data.data.is_required_issue_date );
                            $(".modal-body #is_required_expiry_date").prop( "checked", data.data.is_required_expiry_date );
                            $(".modal-body #is_required_doc_no").prop( "checked", data.data.is_required_doc_no );
                            if(data.data.is_required_issue_date==true)
                            {
                                $(".modal-body #issueDatediv").show();
                                $("#issueDate").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #issueDatediv").hide();
                                $("#issueDate").removeAttr('required');
                            }

                            if(data.data.is_required_expiry_date==true)
                            {
                                $(".modal-body #expiryDatediv").show();
                                $("#expiryDate").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #expiryDatediv").hide();
                                $("#expiryDate").removeAttr('required');
                            }

                            if(data.data.is_required_doc_no==true)
                            {
                                $(".modal-body #docNodiv").show();
                                $("#docNo").attr("required", "required");
                            }
                            else
                            {
                                $(".modal-body #docNodiv").hide();
                                $("#docNo").removeAttr('required');
                            }

                        });

                    });

                    function changeOwned()
                    {
                    var own = $('#owned').val();
                    }


                    $('#first_Nationality').on('change',function()
                    {
                        if( $(this).val()=="leb")
                        {
                            $("#pal").hide();
                            $("#pal1").hide();
                            $("#pal2").hide();
                            $("#pal3").hide();
                            $("#leb").show();
                            $("#kaza").show();
                            $("#country").hide();
                            $("#motherreligion").show();
                            $("#dep_pal_row").hide();
                            $("#dep_leb_row").show();

                        }
                        else if ( $(this).val()=="pal")
                        {
                            $("#motherreligion").hide();
                            $("#pal").show();
                            $("#pal1").show();
                            $("#pal2").show();
                            $("#pal3").show();
                            $("#leb").hide();
                            $("#kaza").hide();
                            $("#country").hide();
                            $("#dep_pal_row").show();
                            $("#dep_leb_row").hide();
                        }
                        else
                        {
                            $("#motherreligion").hide();
                            $("#pal").hide();
                            $("#pal1").hide();
                            $("#pal2").hide();
                            $("#pal3").hide();
                            $("#leb").hide();
                            $("#kaza").hide();
                            $("#country").show();
                            $("#dep_pal_row").hide();
                            $("#dep_leb_row").hide();
                        }

                    });


                    $('#dependent_type').on('change',function()
                    {
                        if( $(this).val()=="child")
                        {
                            $("#depChild").show();
                            $("#depSpouseFields1").hide();
                            $("#depSpouseFields2").hide();
                            $("#depSpouseFields3").hide();
                        }
                        else if ( $(this).val()=="spouse")
                         {
                            $("#depChild").hide();
                            $("#depSpouseFields1").show();
                            $("#depSpouseFields2").show();
                            $("#depSpouseFields3").show();
                        }
                        else
                        {
                            $("#depChild").hide();
                            $("#depSpouseFields1").hide();
                            $("#depSpouseFields2").hide();
                            $("#depSpouseFields3").hide();
                            $("#depFirstRow").hide();
                        }


                    });


                    $(document).ready(function(){

                        var readURL = function(input) {
                            if (input.files & input.files[0])
                             {
                                var reader = new FileReader();

                                reader.onload = function (e)
                                {
                                    $('.profile-pic').attr('src', e.target.result);
                                    $("#reset-profile-pic").removeClass("d-none");
                                    $("#profile-pic-bin").val(e.target.result);
                                }

                                reader.readAsDataURL(input.files[0]);
                                }
                            }

                        $("#profile-pic-upload").on('change', function()
                        {
                            readURL(this);
                        });

                        $("#change-profile-pic").on('click', function()
                        {
                            $("#profile-pic-upload").click();
                        });

                        $("#reset-profile-pic").on('click', function()
                        {
                            $('.profile-pic').attr('src', $('.profile-pic').data('pimg'));
                            $("#reset-profile-pic").addClass("d-none");
                        });


                        $("#myBtn").click(function()
                        {
                            $("#myModal").modal();
                        });

                        $("#docBtn").click(function()
                        {
                            $("#docModal").modal();
                        });

                        $("#add_emergency").click(function()
                        {
                            $("#emergencyModal").modal();
                        });

                        $("#add_ikama").click(function()
                        {
                            $("#ikamaModal").modal();
                        });

                        $("#add_passport").click(function()
                        {
                            $("#passportsModal").modal();
                        });

                        $("#add_company").click(function()
                        {
                            $("#companyModal").modal();
                        });

                        $("#add_qatar").click(function()
                        {
                            $("#qatarModal").modal();
                        });

                        $("#new_request").click(function()
                        {
                            $("#enrollModal").modal();
                        });

                        $("#add_lebanon").click(function()
                        {
                            $("#lebanonModal").modal();
                        });

                    });

                    function openModal(e)
                    {
                        var url='/my/account/document/open/'+e;
                        formValues = $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                            {
                                $(".modal-body #partner_doc_Id").val( data.data.documentId );
                                $(".modal-body #document_type").val( data.data.doctype );
                                $(".modal-body #document_type").prop('disabled', 'disabled');
                                $(".modal-body #is_required_issue_date").prop( "checked", data.data.is_required_issue_date );
                                $(".modal-body #is_required_expiry_date").prop( "checked", data.data.is_required_expiry_date );
                                $(".modal-body #is_required_doc_no").prop( "checked", data.data.is_required_doc_no );
                                if(data.data.is_required_issue_date==true)
                                {
                                     $(".modal-body #issueDatediv").show();
                                     $("#issueDate").attr("required", "required");
                                }
                                else
                                {
                                    $(".modal-body #issueDatediv").hide();
                                    $("#issueDate").removeAttr('required');
                                }

                                if(data.data.is_required_expiry_date==true)
                                {
                                    $(".modal-body #expiryDatediv").show();
                                    $("#expiryDate").attr("required", "required");
                                }
                                else
                                {
                                    $(".modal-body #expiryDatediv").hide();
                                    $("#expiryDate").removeAttr('required');
                                }

                                if(data.data.is_required_doc_no==true)
                                {
                                    $(".modal-body #docNodiv").show();
                                    $("#docNo").attr("required", "required");
                                }
                                else
                                {
                                    $(".modal-body #docNodiv").hide();
                                    $("#docNo").removeAttr('required');
                                }

                                $('#docModal').modal('toggle');
                    });
                    }


                    function submit_info()
                    {
                        var url='/my/account/submit';
                        formValues = $('#info_form').serialize();
                        formValues['im_image'] = $('#profile-pic-upload').val()
                        $.post(url, formValues, function(data)
                        {
                            if(data.status == "success")
                                {
                                    window.scrollTo(0, 0);
                                    $(location).attr('href','/my/home');
                                }
                            else
                                {
                                    window.scrollTo(0, 0);
                                    $('#error_message_div').html("&lt;div class='alert alert-danger' role='alert' >"+data.msg+"&lt;/div>");
                                }

                        });
                    }

                    function save_image()
                    {
                        var url='/my/account/save_image';
                        var formValues= $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                        });
                    }

                    function auto_save()
                    {
                        var url='/my/account';
                        var formValues= $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                        });
                    }

                    function auto_save_refresh()
                    {
                        var url='/my/account';
                        var formValues= $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(location).attr('href','/my/account');
                        });
                    }


                    function save_info()
                    {
                        var url='/my/account';
                        var formValues= $('#info_form').serialize();

                        $.post(url, formValues, function(data)
                        {
                            if(data.status == "success")
                            {
                                window.scrollTo(0, 0);
                                $(location).attr('href','/my/account');
                            }
                        });
                    }

                    $("#save-document-btn").on("submit", function(event)
                    {
                        var url='/my/account/insert_documents';
                        var formValues= $('#doc_form').serialize();
                        $.post(url, formValues, function(data)
                            {
                                if(data.data.status == 'success')
                                    {
                                    $(location).attr('href','/my/account/documents');
                                    }
                            });
                    });


                    function save_ikama()
                    {
                        var url='/my/account/insert_ikama';
                        var formValues= $('#ikama_form').serialize();
                        $.post(url, formValues, function(data)
                            {
                                if(data.data.status == 'success')
                                    {
                                        $(location).attr('href','/my/account/ikama');
                                    }
                            });
                    }

                    function save_emergency()
                    {
                        var url='/my/account/insert_emergency';
                        var formValues= $('#emergency_form').serialize();
                        $.post(url, formValues, function(data)
                            {
                                if(data.data.status == 'success')
                                    {
                                        $(location).attr('href','/my/account/emergency');
                                    }
                             });
                    }


                    function save_company()
                    {
                        var url='/my/account/insert_company';
                        var formValues= $('#comp_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            if(data.data.status == 'success')
                                {
                                    $(location).attr('href','/my/account/company');
                                }
                        });
                    }

                    function save_qatar()
                    {
                        var url='/my/account/insert_qatar';
                        var formValues= $('#qatar_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            if(data.data.status == 'success')
                            {
                            $(location).attr('href','/my/account/qatar');
                            }
                        });
                    }

                    function save_leb()
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
                    }

                    function save_dependant()
                    {
                        var url='/my/account/insert_dependant';
                        var formValues= $('#dep_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            if(data.data.status == 'success')
                            {
                            $(location).attr('href','/my/account/dependants');
                            }
                        });

                    }

                    function openCompanyModal(e)
                    {
                        var url='/my/account/company/open/'+e;
                        formValues = $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(".modal-body #partner_comp_Id").val( data.data.id );
                            $(".modal-body #company_name").val( data.data.company_name );
                            $(".modal-body #street").val( data.data.street );
                            $(".modal-body #job_position").val( data.data.job_position );
                            $(".modal-body #city").val( data.data.city );
                            $(".modal-body #phoneNumber").val( data.data.phoneNumber );
                            $(".modal-body #pobox").val( data.data.pobox );

                            $('#companyModal').modal('toggle');
                        });
                    }

                    function openQatarModal(e)
                    {
                        var url='/my/account/qatar/open/'+e;
                        formValues = $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                        {
                            $(".modal-body #partner_qatar_Id").val( data.data.id );
                            $(".modal-body #city").val( data.data.city );
                            $(".modal-body #street").val( data.data.street );
                            $(".modal-body #qatar_region").val( data.data.qatar_region );
                            $(".modal-body #building").val( data.data.building );
                            $(".modal-body #floor").val( data.data.floor );
                            $(".modal-body #mojama3").val( data.data.mojama3 );
                            $(".modal-body #flat").val( data.data.flat );
                            $(".modal-body #phoneNumber").val( data.data.phoneNumber );
                            $(".modal-body #mobile").val( data.data.mobile );
                            $(".modal-body #pobox").val( data.data.pobox );


                            $('#qatarModal').modal('toggle');
                        });
                    }

                    function update_enroll(ev) {
                        var modal = '#openenrollModal_' + ev
                        $(modal + " .enroll_name").attr('readonly', false);
                        $(modal + " .enroll_cr_number").attr('readonly', false);
                        $(modal + " .enroll_industry").attr("disabled", false);
                        $(modal + " .enroll_phone").attr('readonly', false);
                        $(modal + " .enroll_email").attr('readonly', false);
                        $(modal + " .enroll_website").attr('readonly', false);
                        $(modal + " .update_enroll_id").val($('#enroll_id').val());
                        $(modal + " .add_address_btn").removeClass('d-none');
                        $(modal + " .button_submit").removeClass('d-none');
                        $(modal + " td .delete_address").removeClass('d-none');
                    }

                    function delete_enroll_request(ev) {
                    var url='/my/account/delete_enroll_request/' + ev;
                    $.post(url, function(data)
                    {
                        if(data.status == 'success')
                        {
                            $(location).attr('href','/my/account');
                        }
                        else
                        {
                            alert("Request Already Processed. Please Reload Page.");
                        }

                    });


                    }

                    function openLebanonModal(e)
                    {
                        var url='/my/account/lebanon/open/'+e;
                        formValues = $('#info_form').serialize();
                        $.post(url, formValues, function(data)
                           {
                            $(".modal-body #partner_leb_Id").val( data.data.id );
                            $(".modal-body #region").val( data.data.region );
                            $(".modal-body #owned").val( data.data.owned );
                            $(".modal-body #owned").val( data.data.owned );
                            $(".modal-body #phoneNumber").val( data.data.phoneNumber );
                            $(".modal-body #mobile").val( data.data.mobile );
                            $(".modal-body #flat").val( data.data.flat );
                            $(".modal-body #floor").val( data.data.floor );
                            $(".modal-body #building").val( data.data.building );
                            $(".modal-body #district").val( data.data.district );
                            $(".modal-body #kaza").val( data.data.kaza );
                            $(".modal-body #town").val( data.data.town );
                            $(".modal-body #city").val( data.data.city );
                            $(".modal-body #street").val( data.data.street );

                            $('#lebanonModal').modal('toggle');
                            });
                    }




    });
});
