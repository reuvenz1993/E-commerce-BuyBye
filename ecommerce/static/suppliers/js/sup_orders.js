
function shipping_listener()
{
    $('.shipping').click(function (e) { 
        e.preventDefault();
        w = e
        $('#'+e.target.dataset.edit).show();
        $(this).hide();
    });

    $('.confirm_ship').click(function (e) { 
        e.preventDefault();
        q = e;
        tracking_number = $('#'+e.target.dataset.input_id).val();
        order_id = parseInt(q.target.dataset.order_id)
        $(this).hide();
        $('#'+e.target.dataset.input_id).val();
        $('#'+e.target.dataset.input_id).prop('disabled',true)
        shipment_data = {'order_id':order_id ,
                        'tracking_number' : tracking_number,
                        'make_shipment' : true};
        $.ajax({
            type: "POST",
            url: '/suppliers/sup_orders',
            contentType: 'application/json',
            data : JSON.stringify( shipment_data ),
            success: function (response) {
                successful = response;
                }});
    });
};




function update_order_list(data)
{
    $.ajax({
        type: "POST",
        url: '/suppliers/sup_orders',
        contentType: 'application/json',
        dataType : 'html',
        data : JSON.stringify( data ),
        success: function (response) {
            res = response;
            $('#res_cont').empty().append(res);
            shipping_listener()
            }});
};


function selected_product_list()
{
    res = []
    $('.category_checkbox').each(function()
    {
        if ($(this).is(':checked'))
        {
            val = this.value
            res.push(parseInt(val))
        };
    });

    return res;
}


function selected_status_list()
{
    res = []
    $('.status_item').each(function()
    {
        if ($(this).is(':checked'))
        {
            val = this.value
            res.push(val)
        };
    });

    return res;
};



$('.category_item').change(function (e)
{
    e.preventDefault();
    adjust_filters()
});

function adjust_filters()
{
    filter_data = { 'pid' : selected_product_list(),
                    'status':selected_status_list()}
    if (filter_data["pid"].length > 0 && filter_data["status"].length > 0)
    {
        update_order_list(filter_data);
    } else { $('#res_cont').empty() }
};

adjust_filters();



