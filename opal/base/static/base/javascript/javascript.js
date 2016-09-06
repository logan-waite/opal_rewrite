$(document).ready(function() {
    /************************/
    /* STUFF FOR EVERYTHING */
    /************************/

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


    // Get the app we're using.
    url = window.location.href;
    app = url.split("/");
    console.log(app[3]);

    $("#" + app[3]).addClass('active');

    // Message timouts
    setTimeout(function() {
        $(".alert").fadeOut('slow');
    }, 1500);

    /***************/
    /* CLIENT PAGE */
    /***************/

    // "Add Client" Facebox
    $('#add_client').click(function() {
        load_facebox('add_client');
    })

    // Sort buttons
    $('#az').click(function(event) {
        selected_id = $(".active").val();
        $.post("get_clients/", {sort:'az'}, function(result) {
            $('.list').html(result)
            $('#client-list .list-group-item').each(function() {
                if ($(this).val() == selected_id) {
                    $(this).addClass('active')
                }
            })
        })
    })

    $('#za').click(function() {
        selected_id = $(".active").val();
        $.post("get_clients/", {sort:'za'}, function(result) {
            $('.list').html(result)
            $('#client-list .list-group-item').each(function() {
                if ($(this).val() == selected_id) {
                    $(this).addClass('active')
                }
            })
        })
    })
    // Select the client to view
    $("#client-list").on('click', '.list-group-item:not(.active)', "", function() {
        $(".active", event.delegateTarget).removeClass("active")
        $(this).addClass("active");

        client_id = $(this).val();
        $('#main').load('client_info/', {client:client_id})
    })

    /***************/
    /* EVENT PAGE */
    /***************/

    // "Add Event" Facebox
    $('#add_event').click(function() {
        load_facebox('new_event_form')
    })

    // "Schedule Event" Facebox
    $('#schedule_event').click(function() {
        load_facebox('schedule_event_form');
    })

    // "Edit Events" Facebox
    $('#edit_events').click(function() {
        load_facebox('edit_events');
    })

    // Check off checklist items
    $('.event-block input[type="checkbox"]').click(function() {
        if ($(this).is(':checked')) {
            var checked = 1;
        }
        else {
            var checked = 0;
        }
        var value = $(this).val();
        var image = $(this).closest('ul').siblings('img')

        $.post('save_item_status/', {'checked':checked, 'item_id':value}, function(result) {
            console.log(result)
            if(result == 'complete') {
                image.attr('src', '/static/events/images/complete.png')
            }
            else {
                image.attr('src', '/static/events/images/incomplete.png')
            }
        })
    })

    $('.checklist-dropdown').click(function() {
        var checklist = $(this).siblings('ul')
        var caret = $(this).children('i')
        console.log(caret)
        if (checklist.css('display') == 'none') {
            checklist.slideDown()
            caret.removeClass('rotate-to-90')
            caret.addClass('rotate-to-0')
        }
        else {
            checklist.slideUp()
            caret.removeClass('rotate-to-0')
            caret.addClass('rotate-to-90')
        }
    })

    /***********/
    /* FACEBOX */
    /***********/

    // Facebox
    function load_facebox(url) {
        $('#facebox-content').load(url)
        $('#facebox-back').css('display', 'block')
        $('#facebox').css('display', 'block')
    }

    $('#facebox-close').click(function() {
        $('#facebox-back').css('display', 'none')
        $('#facebox').css('display', 'none')
        $('#facebox-content').html("")
    })

    $('#facebox-back').click(function() {
        $('#facebox-back').css('display', 'none')
        $('#facebox').css('display', 'none')
        $('#facebox-content').html("")
    })
    // Test facebox views

    //$('#facebox-content').load('add_client')

});
