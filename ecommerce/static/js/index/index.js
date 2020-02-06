/*
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
        console.log(this);
        $( this ).attr( "data-product_type" , categories[i][0] );
        $( this ).find('.dark-grey-text').html( categories[i][1] );
        //$( this ).attr( "href" , '/results?category=' + categories[i][0] );
        i = i+1;
        });
    }
});
};

*/

$(document).ready(function () {

    //get_categories()


$('.category').click(function (e) { 
    e.preventDefault();
    //chosen_category = e.currentTarget.getAttribute('data-product_type') ;
    console.log(e);
    a = e;
    location.href =  e.currentTarget.dataset.link;
});

$('#search_submit').click(e =>
    {
    if (search.value != "")
    {
    location.href = '/results?word=' + search.value
    }


    
    });

});

$('#search').keyup(function(e)
{
    if (event.keyCode === 13) {
    e.preventDefault();
    var searchtext = $('#search').val();
    window.location.href = '/results?word=' + searchtext ;
    }
});