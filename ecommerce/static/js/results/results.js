$(document).ready(function () {
    if ( product_list )
    {
        product_list.forEach(product => {
            product_parent = $("<li></li>").addClass('row text-center item align-items-center').attr('id' ,'product num: ' + product[0]).attr('data-pid' ,product[0] ).appendTo($('#products'));
            photo_col = $("<div></div>").attr("id" ,"product_pic" + product[0]).addClass('col').appendTo(product_parent);
            photo = $('<img>').attr("src" , product[8] ).addClass('pic').appendTo(photo_col);
            name_desc_col = $("<div></div>").addClass('col-6 pnt').attr('id' ,product[0]).appendTo(product_parent);
            name_row =$("<div></div>").text(product[1]).addClass('row').appendTo(name_desc_col);
            desc_row =$("<div></div>").text(product[2]).addClass('row').appendTo(name_desc_col);
            price_col = $("<div></div>").text(product[7] + "$").addClass('col').appendTo(product_parent);
            
            
        });
    }

    $(".item").click(function (e) { 
        e.preventDefault();
        console.log(e.currentTarget.dataset.pid);
        pid = e.currentTarget.dataset.pid
        location.href =  '/product2/' + pid;
    });

    if (categories)
    {
    categories.forEach(category => {
        category_li = $("<li></li>").appendTo($('#sidebar_categories'));
        category_a_href = $("<a></a>").attr('data-category' , category).appendTo(category_li);

        })
    }});
