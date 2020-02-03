var categories ;

function get_categories(){
$.ajax({
    type: "POST",
    url: '/get_categories',
    success: function (response) {
        categories = response
        cards = $('.category')

        i = 0
        $( ".category" ).each(function() {
        $( this ).attr( "data-product_type" , categories[i][0] );
        $( this ).find('.dark-grey-text').html( categories[i][1] );
        $( this ).attr( "href" , '/results?category=' + categories[i][0] );
        i = i+1;
        });
    }
});
};



$(document).ready(function () {

    get_categories()


$('.category').click(function (e) { 
    e.preventDefault();
    chosen_category = e.currentTarget.getAttribute('data-product_type') ;
    console.log(chosen_category);
    location.href =  '/results?product_type=' + chosen_category;
});

});