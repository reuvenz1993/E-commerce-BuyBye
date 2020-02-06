$(document).ready(function () {
    
    $('.tgl').click(function (e) { 
        e.preventDefault();
        $('#sup_login_modal , #sup_signup_modal').toggle();
    });
    

});