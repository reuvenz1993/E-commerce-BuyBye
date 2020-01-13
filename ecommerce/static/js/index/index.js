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
        $( this ).attr( "data-category_num" , i );
        $( this ).find('.dark-grey-text').html( categories[i] );
        $( this ).attr( "href" , '/results?category=' + i );
        i = i+1;
        });
    }
});
};



$(document).ready(function () {

    get_categories()

$("#buyer_login_toggle").click(function (e) { 
    e.preventDefault();
    $('#buyer_login_modal').modal('toggle')
});

$('.category').click(function (e) { 
    e.preventDefault();
    chosen_category = e.currentTarget.getAttribute('data-category_num') ;
    console.log(chosen_category);
});

});
