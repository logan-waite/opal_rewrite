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


    $('#sidebar').on('click', '#client-list>.item:not(.active)', function() {
        $('.active').removeClass('active');
        $(this).addClass('active');

        client_id = $(this).val();
        $('#main').load('client_info/', {client:client_id})
    })

    // Sort buttons
    $('#az').click(function(event) {
        selected_id = $(".active").val();
        $.post("get_clients/", {sort:'az'}, function(result) {
            $('#client-list').html(result)
            $('#client-list>.item').each(function() {
                console.log('here')
                if ($(this).val() == selected_id) {
                    $(this).addClass('active')
                }
            })
        })
    })

    $('#za').click(function() {
        selected_id = $(".active").val();
        $.post("get_clients/", {sort:'za'}, function(result) {
            $('#client-list').html(result)
            $('#client-list>.item').each(function() {
                if ($(this).val() == selected_id) {
                    $(this).addClass('active')
                }
            })
        })
    })
})
