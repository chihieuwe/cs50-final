$(document).ready(function(){
    var scrolled = false; // Variable to track scroll state
    $(window).scroll(function(){
        var scroll = $(window).scrollTop();
        var navbar = $(".navbar");
        var navlink = $(".nav-link");
        var navbarBrand = $(".navbar-brand");
        if (scroll > 300) {
            if (!scrolled) {
                navbar.css("background", "#FFC0CB");
                navlink.css("color", "black");
                navbarBrand.css("color", "black");
                scrolled = true;
            }
        } else {
            if (scrolled) {
                navbar.css("background", "transparent");
                navlink.css("color", "rgb(255, 189, 189)");
                navbarBrand.css("color", "rgb(255, 189, 189)");
                scrolled = false;
            }
        }
    });
});