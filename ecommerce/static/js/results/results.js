    /*
    var categories ;

    function get_categories(){
    $.ajax({
        type: "POST",
        url: '/get_categories',
        success: function (response) {
            categories = response
            put_categories();

            }})};
    */
   var category_list = Array();
   var min_price = 0 ;
   var max_price = 10000 ;
   var min_avg = 1 ;
   var word = ""
   var k ;



   
   function load_results()
{
    data = {'category_list' : category_list ,
            'min_price' : min_price ,
            'max_price' : max_price ,
            'min_avg': min_avg}
    
    if ( $('#search').val() != "" )
    {
    data['word'] = $('#search').val()
    };


$.ajax({
    type: "POST",
    url: '/get_search_res',
    contentType: 'application/json',
    dataType : 'json',
    data : JSON.stringify( data ),
    success: function (response) {
        product_list = response;
        console.log(response);
        show_products();
        
        }});
};

function show_products()
{
    $('#products').empty()
    product_list.forEach(product => {
        product_parent = $("<li></li>").addClass('row text-center item align-items-center').attr('id' ,'product num: ' + product.id).attr('data-pid' ,product.id ).appendTo($('#products'));
        photo_col = $("<div></div>").attr("id" ,"product_pic" + product.id).addClass('col').appendTo(product_parent);
        photo = $('<img>').attr("src" , product.picture ).addClass('pic').appendTo(photo_col);
        name_desc_col = $("<div></div>").addClass('col-6 pnt').attr('id' ,product.id).appendTo(product_parent);
        name_row =$("<div></div>").text(product.name).addClass('row').appendTo(name_desc_col);
        desc_row =$("<div></div>").text(product.desc).addClass('row').appendTo(name_desc_col);
        supplier_name_row =$("<div></div>").text(product.supplier.name).addClass('row text-black-50 text-monospace').appendTo(name_desc_col);
        price_col = $("<div></div>").addClass('col font-weight-bold').appendTo(product_parent);
        price_row = $("<div></div>").text(product.price + "$").addClass('row').appendTo(price_col);
        stars_row = $("<div></div>").addClass('row').appendTo(price_col);
        if ( product.orders.count_units )
        {
        order_count_row = $("<div></div>").text( product.orders.count_units +" Sold").addClass('row').appendTo(price_col);
        }
        if ( product.reviews.avg )
        {
            $(stars_row).append(product.reviews.avg + " ");
            $(stars_row).append("<div class='icon'><i class='far fa-star' aria-hidden='true'></i></div>");
            $(stars_row).append( product.reviews.count  +" reviews" );
        }
        $(product_parent).click(function (e) { 
            e.preventDefault();
            pid = e.currentTarget.dataset.pid
            location.href =  '/product2/' + pid;
            
        });
    });
};

$(document).ready(function () {

    $('#search').keyup(function (e) { 
        e.preventDefault();
        load_results();
            
        });


    $.ajax({
        type: "POST",
        url: '/get_categories',
        success: function (response) {
            categories = response
            //put_categories();
            put_categories2()

            }});
/*
    if ( product_list )
    {
        show_products();

    }
*/



    function put_categories(){
        console.log('put cat runing');
        if (categories)
        {
        categories.forEach(category => {
            category_li = $("<li></li>").addClass('filter_category').css('cursor' , 'pointer').attr('data-category' , category[1]).text(category[1]).appendTo($('#sidebar_categories'));
            category_items= $("<span></span>").addClass('close text-black-50').text(category[2]).appendTo(category_li);
            
        })
        select_category();
        }};

        function put_categories2(){
            console.log('put cat runing');
            if (categories)
            {
                categories.forEach(category => {
                    category_li = $("<li></li>").addClass('checkbox filter_category').css('cursor' , 'pointer').appendTo($('#sidebar_categories'));
                    checkbox_labal = $("<label></label>").text(category[1]).appendTo(category_li);
                    checkbox =$("<input type='checkbox' checked>").attr('value' , category[0]).attr('data-category' , category[0]).addClass('category_checkbox category_item').prependTo(checkbox_labal);
                    category_items= $("<span></span>").addClass('close text-black-50').text(category[2]).appendTo(category_li);
            });
                get_list();
                load_results()
            }};



    function get_list(){

        categories.forEach(category =>
        {
            category_list.push(category[0]);
            });
        $('.category_item').change(function (e)
        {
            e.preventDefault();

            if ( $('#search').val() != "" )
            {
                word = $('#search').val()
            }

            category_list = selected_category_list()
            min_price = parseInt(  $('#min').val() );
            max_price = parseInt(  $('#max').val() );
            min_avg = parseInt ( $("input[type='radio']:checked").val() );
            load_results()
        });
    };






function selected_category_list()
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



    function select_category(){
    $('.filter_category').click(function (e) {
        e.preventDefault();
        filter_product_type = e.currentTarget.dataset.category;
        console.log(filter_product_type);
        $('#current_cat').html(filter_product_type);
        $('#current_cat_view , #sidebar_categories').toggle();
        //update_view();

        });
    };

    $('#go_back_cat').click(function (e) { 
        e.preventDefault();
        $('#current_cat').html('all');
        $('#current_cat_view , #sidebar_categories').toggle();
        //update_view();
    });
/*
    $('#min , #max').click(function (e) { 
        e.preventDefault();
        filter_product_type = "";
        min_price = $('#min').val()
        max_price = $('#max').val()
        console.log('min' + min_price)
        console.log('max' + max_price)
    });*/


    $("input[type='radio'] , #min , #max").change(function (e) { 
        e.preventDefault();
        console.log('change');
        //update_view();

    });

    function update_view()
    {
        min_stars = $("input[type='radio']:checked").val();
        min_price = $('#min').val();
        max_price = $('#max').val();
        product_type = $('#current_cat').html();
        data = [];
        data['product_type'] = product_type;
        data['min_price'] = min_price;
        data['max_price'] = max_price;
        data['max_price'] = min_stars;
        console.log('update_view_run');
        console.log(data);

        $.ajax({
            type: "POST",
            url: "/get_results",
            data: {'product_type' : product_type , 'min_price' :min_price , 'max_price': max_price ,'min_stars' : min_stars },
            success: function (response) {
                console.log(response);
                b = 555;
                product_list = response
                show_products();
            }
        });
    };
    
/*
    function update_view()
    {
        
    }*/
/*
    setTimeout(handle_click , 1500);

    function handle_click(){
    $(".item").click(function (e) { 
        e.preventDefault();
        console.log(e.currentTarget.dataset.pid);
        pid = e.currentTarget.dataset.pid
        location.href =  '/product2/' + pid;
    });
};
*/






});
