qty = $('#qty').val();
$(document).ready(function ()
{
    if ( product )
    {
        $("#name").html(product.name);
        $("#desc").html(product.desc);
        $("#price").html(product.price + ' $');
        $('.product_pic').attr('src' , product.picture );
        $("#brand").html(product.brand );
        $("#seller").html(product.supplier.name);
        $("#sold").html(product.orders.count_units);
        $("#more_info").html(product.Additional_information);
        
        
        if (product.reviews.count > 0)
        {
            $("#stars").html("")
            $("#stars").append("<div class='icon'>" + product.reviews.avg +  "<i class='far fa-star' aria-hidden='true'></i>" + "  , " + product.reviews.count + " reviews" + "</div>");
        }




    };


    if ( product.reviews.count )
    {
        product.reviews.get_review.forEach(rev => {
            product_parent = $("<li></li>").addClass('row text-center review').attr('id' ,'product num: ' + rev.id).appendTo($('#reviews'));
            stars = $("<div></div>").text("Rank :" + rev.stars ).addClass('col').appendTo(product_parent);
            review = $("<div></div>").addClass('col-6 pnt').attr('id' ,rev.id).appendTo(product_parent);
            review_content =$("<div></div>").text(rev.review_content).addClass('row').appendTo(review);
            reviewer_name =$("<div></div>").text('by: ' + rev.reviewer).addClass('row').appendTo(review);
            review_time = $("<div></div>").text(rev.review_time.slice(5,16)).addClass('col').appendTo(product_parent);

        });
    }

    setTimeout(handlers,1000);

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
                    alart = $('<div></div>').text('order confirm').addClass('alert alert-success text-center').prependTo('#cont_product');
                    $('#items_count').text(response['cart_size'])
                    $('#cart_success').modal('show');

                    $('#continue_shopping').click( () => {
                        $('#cart_success').modal('hide');
                    });

                    $('#View_Shopping_Cart').click( () => {
                        window.location.href = '/'
                    });                    
                    
                    }});
            
            });


    };



});


