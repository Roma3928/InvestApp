$(function() {

    $('.d-flex [href]').each(function (){
        if (this.href == window.location.href) {

            if ($(this).hasClass("text-black") == false){
                     $(this).addClass('text-white');
            }
        }
    });


});


