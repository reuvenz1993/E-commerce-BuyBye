

    $("#file").change(function() {
        readURL(this);
        });
    
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e)
            {
            $('#img').attr('src', e.target.result);
            $('#preview').css('display' , 'block');
            }
            reader.readAsDataURL(input.files[0]);
        }
        };













$('.change').click(function(e)
{
a = e
$(e.target ).toggle();
$('#'+a.target.dataset.sibling).toggle()
$('#'+ e.target.dataset.change).prop('disabled', function (_, val) { return ! val; });


});


$('.confirm').click(function(e)
{
a = e

val = $('#'+a.target.dataset.change).val();
console.log(val);
change = update_product_info ( product.id , e.target.dataset.change , val );
change.then( () =>
{
    console.log('yay');
    //alert = $("<div></div>").attr('role','alert').addClass('alert alert-success').text('This is a success')
    //$('#cont_product').prepend(alert);
    console.log(e);
    $('#'+ e.target.dataset.sibling).toggleClass('fa-check fa-edit');
    $('#'+ e.target.dataset.change).css('background-color' , 'lightgreen');
    setTimeout(function()
    {
        $('#'+ e.target.dataset.sibling).toggleClass('fa-check fa-edit');
        $('.form-control').css('background-color' , '');
    }, 1200);
});
});



$("#but_upload").click(function(){

    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);
    fd.append('pid',product.id  )

    $.ajax({
        url: '/edit_product_pic',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        dataType: 'json',
        success: function(response)
        {
            console.log(response);
            res = response;
            console.log(res);
            $('#product_img').attr('src', response[1] )
            $('#preview').css('display' , 'none');
        }});
    });







function update_product_info(product_id , input , value)
{
    return new Promise((resolve, reject) =>
    {
        data = {'product_id':product_id,
                'input':input,
                'value' :value};

        console.log(data)

        $.ajax({
            type: "POST",
            url: '/supplier_update_product',
            contentType: 'application/json',
            data:JSON.stringify (data),
            dataType : "json" ,
            success: function (response)
                {
                console.log(response);
                if (response[0] == true) {resolve(response);}
                else {reject(response);};
                }
        });
    });
};