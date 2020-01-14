$(document).ready(function () {
    if ( product_data )
    {
        $("#name").html(product_data[1]);
        $("#desc").html(product_data[2]);
        $("#price").html(product_data[7] + ' $');
        $('#product_img').attr('src' , product_data[8] );
    };


    if ( reviews )
    {
        reviews.forEach(reviews => {
            product_parent = $("<li></li>").addClass('row text-center review').attr('id' ,'product num: ' + reviews[0]).appendTo($('#reviews'));
            stars = $("<div></div>").text("Rank :" + reviews[2] ).addClass('col').appendTo(product_parent);
            review = $("<div></div>").addClass('col-6 pnt').attr('id' ,reviews[0]).appendTo(product_parent);
            review_content =$("<div></div>").text(reviews[3]).addClass('row').appendTo(review);
            reviewer_name =$("<div></div>").text('by: '+ reviews[5]).addClass('row').appendTo(review);
            review_time = $("<div></div>").text(reviews[4].slice(5,16)).addClass('col').appendTo(product_parent);

        });
    }



});