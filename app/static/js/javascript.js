(function() {
    
    $('.saves, .unsaves').click(function(e) {
        var class_ = $(this).attr('class');
        console.log("before ajax");

        $.ajax({
            data: {recipeID: id, action:class_},
            type: 'POST',
            url: '/saves',
        });
        console.log("after ajax");

        if (class_ == 'unsaves') {
            $(this).attr('class' ,'saves');
            $(this).text('Save');
            console.log("unsave to save");
        } else {
            $(this).attr('class' ,'unsaves');
            $(this).text('Unsave');
            console.log("save to unsave");
        }
        e.preventDefault();

    });
});