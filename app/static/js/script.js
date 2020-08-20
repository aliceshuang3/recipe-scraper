$('document').ready(function (){
    $('.saves, .unsaves').click(function(e) {
        var id = $(this).attr('id');
        // get rid of "save" word from recipeResults.html id name
        id = id.slice(4);
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

function byID(id) {
    return document.getElementById(id);
}

function startToggle(n) {
    // get the specific id of the container
    containerId = "container" + n.toString();
    saveLinkId = "save" + n.toString();
    saveBtnId = "btnsave" + n.toString();
    // hide save button and link when user clicks open recipe pop-up
    const link = byID(saveLinkId);
    const btn = byID(saveBtnId);

    // add or remove the "closed" class to toggle opening/closing
    if (byID(containerId).classList.contains("closed")) {
        byID(containerId).classList.remove("closed");
    } else {
        byID(containerId).classList.add("closed");
    }

    if (link.style.display === "none") {
        link.style.display = "block";
        btn.style.display = "block";
    } else {
        link.style.display = "none";
        btn.style.display = "none";
    }

}

// back to top button on results page----------------------------------------
// Reference: https://codepen.io/matthewcain/pen/ZepbeR

// call after elements on page have loaded
window.onload = function(){
  var btn = $("#to-top-button");

  $('div.search-results-page').scroll(function() {

    // if any scrolling happened, show the button
    y = $('div.search-results-page').scrollTop();
    if (y > 0) {
      btn.addClass('show');
    } else {
      btn.removeClass('show');
    }
  });

  // on button click, go back to the top of page
  btn.on('click', function(e) {
    e.preventDefault();
    $('div.search-results-page').animate({scrollTop:0}, '300');
  });
};

