/*$(document).ready(function () {

    setTimeout(do_stuff , 1500);

    function do_stuff()
    {
        put_categories();
    }

    function put_categories(){
        console.log('put cat runing');
        if (categories)
        {
        categories.forEach(category => {
            category_li = $("<li></li>").addClass('filter_category').css('cursor' , 'pointer').attr('data-category' , category).text(category).appendTo($('#sidebar_categories'));
        })
        make_categories_clickable();
        }};


    function make_categories_clickable(){
    $('.filter_category').click(function (e) { 
        e.preventDefault();
        category = e.currentTarget.dataset.category;
        console.log(category);
    })
    };


    } );
