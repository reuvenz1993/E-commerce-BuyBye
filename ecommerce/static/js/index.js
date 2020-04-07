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

    $('#search').keyup(function(e)
{
    if (event.keyCode === 13) {
    e.preventDefault();
    var searchtext = $('#search').val();
    window.location.href = '/results?word=' + searchtext ;
    }
});


});

