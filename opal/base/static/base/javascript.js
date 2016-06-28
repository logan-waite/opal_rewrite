$(document).ready(function() {

    // Get the app we're using.
    url = window.location.href;
    app = url.split("/");
    console.log(app[3]);

    $("#" + app[3]).addClass('active');

    setTimeout(function() {
        $(".alert").fadeOut('slow');
    }, 1500);
});
