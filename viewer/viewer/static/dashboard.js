
/* globals Chart:false, feather:false */
$(document).ready(function() {
    feather.replace();
    $('nav a').removeClass('active');
    $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
    $(".nav .nav-link").on("click", function(){
        console.log('click 1')
        $(".nav").find(".active").removeClass("active");
        $(this).addClass("active");
    });
})
