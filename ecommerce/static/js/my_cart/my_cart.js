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


    $("[data-type='message']").change( (e) =>
    {
        data = {'type': 'update_buyer_message', 'item_id': e.target.dataset.item_id, 'buyer_message': e.target.value};
        buy_button = $("[data-type='buy_this'][data-item_id="+data['item_id']+"]");
        buy_button.removeClass('buy_this');

        update = update_buyer_message(data);
        update.then(()=>
        {
            buy_button.addClass('buy_this');
        })

    });

    function update_buyer_message(data)
    {
    return new Promise((resolve)=>
        {
            $.ajax({
                type: "GET",
                url: '/my_cart',
                data : data ,
                success: function (response) {
                    resolve(response)
                    }});
        });
    };

});