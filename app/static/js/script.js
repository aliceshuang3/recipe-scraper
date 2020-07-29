$('document').ready(function (){ 
    $('.saves, .unsaves').click(function(e) {
        var id = $(this).attr('id');
        var class_ = $(this).attr('class');

        $.ajax({
            data: {recipeID: id, action:class_},
            type: 'POST',
            url: '/saves',
        });

        if (class_ == 'unsaves') {
            $(this).attr('class' ,'saves');
            $(this).text('Save');
        } else {
            $(this).attr('class' ,'unsaves');
            $(this).text('Unsave');
        }
        e.preventDefault();

    });
});