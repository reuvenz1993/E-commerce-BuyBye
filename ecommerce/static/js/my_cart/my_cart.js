$(document).ready(function () {
    
    $("#change_shipping_info").click(function (e) { 
        e.preventDefault();
        $("#address , #to").prop("disabled", false);
        
    });


setTimeout( show_items ,1000);


    function show_items()
    {
        cart.cart.forEach( item =>
            {
                product_list_item = $('<div></div>').addClass('card-footer product_list_item').appendTo($("#products"));
                product_name =$('<div></div>').attr("id" ,"product_name id :" + item.id).addClass('row text-center justify-content-center h4').text(item.product.name).appendTo(product_list_item);
                product_main =$('<div></div>').addClass('justify-content-center row text-center').appendTo(product_list_item);
                $('<div></div>').addClass('col-3').appendTo(product_main).append($('<img>').attr('src', item.product.picture).css('max-width','125px') );
                col_mid =$('<div></div>').addClass('col mid').appendTo(product_main);
                $('<div></div>').addClass('row justify-content-center').text(item.product.desc).appendTo(col_mid);
                btn_div =$('<div></div>').attr("id" ,item.id).addClass('col-3').css('max-width','125px').appendTo(product_main);
                Buy_this =$("<button></button>").attr("data-item_id" ,item.id).addClass('btn btn-sm row buy_this btn_radius').text("Buy this").appendTo(btn_div);
                Buy_this.click(e => {window.location.href = '/cart_actions?type=buy_one&&item_id=' + item.id;  })
                remove = $("<button></button>").attr("data-item_id" ,item.id).addClass('btn btn-sm row remove_this btn_radius').text("Remove").appendTo(btn_div);
                remove.click(e => {window.location.href = '/cart_actions?type=remove&&item_id=' + item.id;  })
                cart_main =$('<div></div>').addClass('row').appendTo(product_list_item);
                $('<div></div>').addClass('col').text("Qty : " + item.qty).appendTo(cart_main);
                $('<div></div>').addClass('col').text("Price : " + item.unit_price).appendTo(cart_main);
                $('<div></div>').addClass('col').text("Total : " + item.total + " $ ").appendTo(cart_main);



            });
    };

    $("#total_price").html(cart.total_cart_price);

});