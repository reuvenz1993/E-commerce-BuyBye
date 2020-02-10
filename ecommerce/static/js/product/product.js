qty = parseInt($('#qty').val());
page = 1
$(document).ready(function ()
{

    setTimeout(init,500);

    function init()
    {
        handlers();
        order_or_cart();
        buy_now()

    };

    function handlers()
    {
        console.log('test')
        $('#total').val(product.price);
        total_price = qty * product.price;
        $('#qty').change(function (e) {
            e.preventDefault();
            qty = $('#qty').val();
            total_price = qty * product.price;
            $('#total').val(total_price);



        });


        $('#add_to_cart').click( () => {
            data = { 'type' : 'cart' , 'product_id' : product.id , 'qty' : qty };

            $.ajax({
                type: "POST",
                url: '/buy_now_or_cart',
                contentType: 'application/json',
                dataType : 'json',
                data : JSON.stringify( data ),
                success: function (response) {
                    product_list = response;
                    console.log(response);
                    $('#buy_now_modal').hide();
                    $('#buy_now').hide();
                    $('#add_to_cart').hide();
                    $('#qty').prop( 'disabled' , 'true' );
                    alert = $('<div></div>').text('Item added to cart').addClass('alert alert-success text-center').prependTo('#cont_product');
                    $('#items_count').text(response['cart_size'])
                    $('#cart_success').modal('show');

                    $('#continue_shopping').click( () => {
                        $('#cart_success').modal('hide');
                    });

                    $('#View_Shopping_Cart').click( () => {
                        window.location.href = '/results'
                    });
                    }});
            });



    $('[data-page_number]').click((e)=>
    {
    page = e.currentTarget.dataset.page_number;
    search_products()
    });

    };

    function order_or_cart()
{   
    console.log('order_or_cart run');
    $('#checkout').click( (e) => {

        console.log(e)
        data = { 'type' : 'buy' , 'product_id' : product.id , 'qty' : qty , 'buyer_message' : $('#buyer_message').val() };
        console.log('order_or_cart')
        
        $.ajax({
            type: "POST",
            url: '/buy_now_or_cart',
            contentType: 'application/json',
            dataType : 'json',
            data : JSON.stringify( data ),
            success: function (response) {
                temp = response;
                console.log(temp);
                $('#buy_now_modal').hide();
                $('#buy_now').hide();
                $('#add_to_cart').hide();
                $('#qty').prop( 'disabled' , 'true' );
                alert = $('<div></div>').html(temp.product_name +' Ordered successfully - Order id :' + "<a href='/account?focus_order="+temp.order_id+"'>" + temp.order_id + "</a>").addClass('alert alert-success text-center').prependTo('#cont_product');
                }});
        
        });
};


    function buy_now()
    {



        if (typeof current_user === 'undefined' || current_user === null)
        {
            $("#buy_now , #add_to_cart").attr("disabled", true);
            $("#buy_now , #add_to_cart").click(()=>
            {
                $('#buyer_signup_modal').modal('toggle');
            })
        } else
        {
            //$('#customer_name').val(current_user.name);
            //$('#order_address').text(current_user.address);
        };

        $("#buy_now").click(function (e)
        {
            e.preventDefault();

            $('#edit').click(function()
            {
                $('#order_address').attr("disabled", false);
                $('#customer_name').attr("disabled", false);
            });

            $('#order_qty').text(qty);
            $('#order_unit_price').text(product.price);
            $('#order_total').text(total_price);

            $('#buy_now_modal').modal('toggle');
            qty = $('#qty').val();
            total_price = qty * product.price;
            $("#step1").click(function (e)
            {
                $('#collapseOne').removeClass('show');
                $('#collapseTwo').addClass('show');
            });

            $("#stap2").click(function (e)
            {
                $('#collapseTwo').removeClass('show');
                $('#collapseThree').addClass('show');
                $('#order_qty').text(qty);
                $('#order_unit_price').text(product.price);
                $('#order_total').text(total_price);
            });



        });

    };

});

