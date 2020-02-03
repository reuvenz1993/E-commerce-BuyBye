$(document).ready(function ()
{
    

$("#buyer_login_toggle").click(function (e)
    {
    e.preventDefault();
    $('#buyer_login_modal').modal('toggle');
    });

    $("#buyer_signup_toggle").click(function (e)
    {
    e.preventDefault();
    $('#buyer_signup_modal').modal('toggle');
    });



});