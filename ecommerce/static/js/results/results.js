$(document).ready(function () {
    if ( product_list )
    {
        product_list.forEach(product => {
            product_parent = $("<li></li>").addClass('row text-center item').attr('id' ,'product num: ' + product[0]).appendTo($('#products'));
            photo_col = $("<div></div>").text("photo").addClass('col').appendTo(product_parent);
            name_desc_col = $("<div></div>").addClass('col-6 pnt').attr('id' ,product[0]).appendTo(product_parent);
            name_row =$("<div></div>").text(product[1]).addClass('row').appendTo(name_desc_col);
            desc_row =$("<div></div>").text(product[2]).addClass('row').appendTo(name_desc_col);
            price_col = $("<div></div>").text(product[7] + "$").addClass('col').appendTo(product_parent);

        });
    }

    $(".pnt").click(function (e) { 
        e.preventDefault();
        pid = e.currentTarget.id
        location.href =  '/product?category=' + pid;
    });
});
