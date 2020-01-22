$(document).ready(function () {


    if (typeof current_user === 'undefined' || current_user === null)
    {
        $("#buy_now , #add_to_cart").attr("disabled", true);
    } else
    {
        $('#customer_name').val(current_user.buyer.name);
        $('#order_address').text(current_user.buyer.address);
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
    
    
        $('#customer_name').text('TBD');
        $('#address').text('TBD');
        seller_name = $("<div></div>").text("Seller  : " + product.supplier.name ).addClass('col').appendTo($('#order_seller'));
        seller_rank = $("<div></div>").text("Average rank  : " + product.supplier.supplier_avg_stars ).addClass('col').appendTo($('#order_seller'));
        seller_name = $("<div></div>").text("Seller  : " + product.supplier.name ).addClass('col').appendTo($('#order_seller'));
        product_name = $('<h3></h3>').text(product.name).appendTo($('#product_name'))
        product_pic_col = $("<div></div>").addClass('col').appendTo($('#product'));
        photo = $('<img>').attr("src" , product.picture ).addClass('pic').appendTo(product_pic_col);
        product_desc = $("<div></div>").text(product.desc ).addClass('col align-self-md-center').appendTo($('#product'));
        seller_name = $("<div></div>").text("Units sold  : " + product.orders.count_units ).addClass('col').appendTo($('#stats'));
        seller_name = $("<div></div>").text("Rank  : " + product.reviews.avg ).addClass('col').appendTo($('#stats'));


        $('#chackout').click(function (e) { 
            e.preventDefault();
            data = { pid : product.id , qty : qty }

            
        });

    });


});


