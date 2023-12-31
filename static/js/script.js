$(document).ready(function(){
    var scrolled = false; // Variable to track scroll state
    $(window).scroll(function(){
        let scroll = $(window).scrollTop();
        let navbar = $(".navbar");
        let navlink = $(".nav-link");
        let navbarBrand = $(".navbar-brand");
        let credential = $(".credential");
        if (scroll > 300) {
            if (!scrolled) {
                navbar.css("background", "#FFC0CB");
                navlink.css("color", "black");
                navbarBrand.css("color", "black");
                credential.css("color", "black");
                scrolled = true;
            }
        } else {
            if (scrolled) {
                navbar.css("background", "transparent");
                navlink.css("color", "rgb(255, 189, 189)");
                navbarBrand.css("color", "rgb(255, 189, 189)");
                credential.css("color", "rgb(255, 189, 189)");
                scrolled = false;
            }
        }
    });
    $('#service').change(function() {
        var price = $(this).find(':selected').data('price');
        if (price) {
            $('#price').text('Price: ' + price);
            $('#hiddenPrice').val(price);
        } else {
            $('#price').text('');
        }
    }).change(); // Trigger the change event immediately
    $('.image-modal-trigger').click(function() {
        // Get the image source from the data attribute
        let imgSrc = $(this).data('imgsrc');
        
        // Set the source for the image in the modal
        $('#modal-image').attr('src', imgSrc);
        
        // Show the modal
        $('#modal').show();
    });
});

