$(document).ready(function() {
    // Setup CSRF token stuff for AJAX
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var csrftoken = getCookie('csrftoken');

    // Get the app we're using.
    url = window.location.href;
    app = url.split("/");
    console.log(app[3]);

    $("#" + app[3]).addClass('active');

    // Message timouts
    setTimeout(function() {
        $(".alert").fadeOut('slow');
    }, 1500);

    // Facebox
    $('#facebox-back').click(function() {alert("hi")})
    $('#add_client').click(function() {
        alert('adding')
    })


});
