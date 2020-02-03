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
                        $('#s'+e.target.id).text('closed');
                        e.target.remove();
                    } else 
                    {
                        console.log('order confirm error');
                    }
                }
            });


    //window.location.href = '/account?confirm_id=' + e.currentTarget.dataset.order_id;
    });

});