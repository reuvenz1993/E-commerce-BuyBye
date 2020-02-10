page = 1
$(document).ready(function () {

    $("#name_input_edit").click(function (e) {
        e.preventDefault();
        $("#name_input_edit").prop("disabled" , true)
        $("#name_input_confirm , #name_input").prop("disabled" , false)
    });

    $("#name_input_confirm").click(function (e) {
        e.preventDefault();
        $("#name_input_edit").prop("disabled" , false)
        $("#name_input_confirm , #name_input").prop("disabled" , true)
        update_personal('name' , $('#name_input').val())



    });

    $("#address_input_edit").click(function (e) { 
        e.preventDefault();
        $("#address_input_edit").prop("disabled" , true)
        $("#address_input_confirm , #address_input").prop("disabled" , false)
    });

    $("#address_input_confirm").click(function (e) { 
        e.preventDefault();
        $("#address_input_edit").prop("disabled" , false)
        $("#address_input_confirm , #address_input").prop("disabled" , true)
        update_personal('address' , $('#address_input').val() )
    });


    function update_personal( field , value)
    {
        data = { type : 'personal' };
        data[field] = value;

        $.ajax({
            type: "POST",
            url: "/account_actions",
            contentType: 'application/json',
            data: JSON.stringify (data),
            dataType : "json" ,
            success: function (response) {
                console.log(response);
                
            }
        });
    }
    







});


function orders_init()
{
    $('[data-page_number]').click((e)=>
    {
    page = e.currentTarget.dataset.page_number;
    $.ajax({
        type: "POST",
        url: '/account',
        contentType: 'application/json',
        dataType : 'html',
        data : JSON.stringify( {'page': page} ),
        success: function (response)
            {
            res = response;
            $("#order_list").empty().append(response);
            $('html, body, .container').animate(
                {
                scrollTop: $("#order_list").offset().top-90}, 1500);
            }
    })
    });

    

    $(".confirm").click( e =>
        {
            console.log(e);
            data = { type : 'confirm' , id : e.currentTarget.dataset.order_id };

            $.ajax({
                type: "GET",
                url: "/account_actions",
                data: data,
                success: function (response) {
                    console.log(response)
                    if ( response == true )
                    {
                        $('#s'+e.currentTarget.dataset.order_id).text('Finished');
                        e.target.remove();
                    } else 
                    {
                        console.log('order confirm error');
                    };
                }
            });
    });

    $(".review").click( e =>
        {
            review_order = e.currentTarget.dataset.order_id

            $('.star').click((e)=>
            {
                $('#review_text').show();
            });
        })



};

orders_init()


function send_review(data)
{
    return new Promise((resolve) =>
    {

        $.ajax({
        type: "POST",
        url: '/account',
        contentType: 'application/json',
        dataType : 'json',
        data : JSON.stringify( data ),
        success: function (response)
            {
            console.log(response);
            resolve(response);
            }
        });

    });
};

$("#submit_review").click((e)=>
        {
            console.log("submit review run");
            console.log(e);

            data = {'order_id': review_order,
                    'stars':$("input[type='radio']:checked").val(),
                    'review_content':$("#review_text").val()};

        send = send_review(data);
        send.then(() =>
            {
                $('#exampleModalCenter').modal('toggle');
                $("input[type='radio']:checked").prop('checked', false);
                $('#review_text').val('');
                $('.review[data-order_id='+review_order+']').remove();
                console.log("submit review done");
            });

        });