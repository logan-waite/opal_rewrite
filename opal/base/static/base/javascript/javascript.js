var title_suffix = " | OPAL";

function titleCase(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

$(function() {
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

    var csrftoken = getCookie('csrftoken');

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

    // This is for the loading icon that comes up when switching pages


    // This is going to be all the stuff for changing pages (one-page app)
    $('.sidebar-menu li a').click(function(e) {
      e.preventDefault();
      var href = $(this).attr("href")
      var page = $(this).attr("href").split(" ")[0].slice(1)
      // Change the title
      $('head title').text(titleCase(page + title_suffix))
      // Change the page header
      $('.content-header h1').text(titleCase(page))
      // Load the page
      $('.content .row').load(href)
    })

})
