$(document).ready(function(){
    $('#wrapwrap #top .navbar-light').removeClass('bg-light');
    $('#wrapwrap #top .navbar-expand-md').removeClass('navbar-light');
    if ((window.location.href.indexOf("login") > -1) || (window.location.href.indexOf("signup") > -1) || (window.location.href.indexOf("reset_password") > -1)){
       console.log("###");
       $("main").addClass("bglogin");
    }

    $('.owl-carousel.management_item_slider').owlCarousel({
                          autoplay: true,
                         autoplayTimeout: 5000000,
                         autoplayHoverPause: true,
                         loop: true,
                         margin:20,
                         nav: true,
                         navigation: true,

                         responsive: {
                             0: {
                                 items: 1
                             },
                             600: {
                                 items: 2
                             },
                             992: {
                                 items: 2
                             }
                             }

                     })


//    $('.datepicker').datepicker({
//        dateFormat: 'dd/mm/yy',
//    });

  $(document).on('click', '[data-toggle="lightbox"]', function(event) {
                        event.preventDefault();
                        $(this).ekkoLightbox();
                        });


});


