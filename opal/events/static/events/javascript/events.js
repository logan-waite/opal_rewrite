$(document).ready(function() {
    // Set up calendar
    $('#calendar').fullCalendar({
        header: {
            left: "prev,next today",
            center: "title",
            right: "month agendaWeek agendaDay"
        },
        theme: false,
        events: {
            url: "/events/get_scheduled_events",
            complete: function(data) {
                console.log(data);
            }
        }
    })
})
