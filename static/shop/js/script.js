$(document).ready(function() {
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:false,
        dots:false,
        stagePadding:100,
        autoplay:true,
        autoplayTimeout:7000,
        autoplayHoverPause:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }
    });

    $('.toast').toast('show');

});