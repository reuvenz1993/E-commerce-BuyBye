$(document).ready(function () {

    console.log('rff');

    if (typeof current_user === 'undefined' || current_user === null)
    {
        $("#buy_now , #add_to_cart").attr("disabled", true);
    } else
    {
        //$('#customer_name').val(current_user.name);
        //$('#order_address').text(current_user.address);
    }

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
    
    
        //$('#customer_name').text('TBD');
        //$('#address').text('TBD');
        //seller_name = $("<div></div>").text("Seller  : " ).addClass('col').appendTo($('#order_seller'));
        //seller_rank = $("<div></div>").text("Average rank  : " ).addClass('col').appendTo($('#order_seller'));
        //seller_name = $("<div></div>").text("Seller  : " ).addClass('col').appendTo($('#order_seller'));
        //product_name = $('<h3></h3>').text("product.name").appendTo($('#product_name'))
        //product_pic_col = $("<div></div>").addClass('col').appendTo($('#product'));
        //photo = $('<img>').attr("src" , "product.picture" ).addClass('pic').appendTo(product_pic_col);
        //product_desc = $("<div></div>").text(product.desc ).addClass('col align-self-md-center').appendTo($('#product'));
        //seller_name = $("<div></div>").text("Units sold  : " ).addClass('col').appendTo($('#stats'));
        //seller_name = $("<div></div>").text("Rank  : " ).addClass('col').appendTo($('#stats'));


        setTimeout(order_or_cart,500);

function order_or_cart()
{   
    console.log('order_or_cart run');
    $('#chackout').click( (e) => {

        console.log(e)
        data = { 'type' : 'buy' , 'product_id' : product.id , 'qty' : qty };
        
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
                alert = $('<div></div>').text('Order Confirmed').addClass('alert alert-success text-center').prependTo('#cont_product');
                //$('#cart_success').modal('show');
                
                }});
        
        });



};



    });


});


