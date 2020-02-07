$(document).ready(function () {

    $("#change_shipping_info").click(function (e) { 
        e.preventDefault();
        $("#address , #to").prop("disabled", false);
    });


    $('.buy_this').click(e =>
        {
            window.location.href = '/my_cart?type=buy_one&&item_id=' + e.currentTarget.dataset.item_id;
        });

    $('.remove_this').click(e =>
        {
            window.location.href = '/my_cart?type=remove&&item_id=' + e.currentTarget.dataset.item_id;
        });
});