import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event, Place, Scheduled_Event

# Create your views here.
@login_required
def index(request):
    data = {}

    scheduled_events = Scheduled_Event.objects.order_by('start').all()

    for event in scheduled_events:
        # Format dates to be readable for the user
        # Start Date
        start = str(event.start).split(" ")
        start_date = time.strftime('%m/%d', time.strptime(start[0], '%Y-%m-%d'))
        event.start = start_date
        # End Date
        end = str(event.end).split(" ")
        end_date = time.strftime('%m/%d', time.strptime(end[0], '%Y-%m-%d'))
        event.end = end_date


    data['events'] = scheduled_events

    return render(request, 'events/index.html', data)

@login_required
def new_event_form(request):
    return render(request, 'events/new_event_form.html')

@login_required
def new_event_submit(request):
    name = request.POST['name']
    description = request.POST['description']
    price = request.POST['price']

    try:
        event = Event(
            name=name,
            description=description,
            price=price
        )
        event.save()

        messages.success(request, "Your event was saved successfully.")
    except:
        messages.error(request, "There was an error saving your event.")

    return redirect('events:index')

@login_required
def schedule_event_form(request):
    data = {}
    data['events'] = Event.objects.order_by('name').all()
    data['places'] = Place.objects.order_by('name').all()

    return render(request, 'events/schedule_event_form.html', data)

@login_required
def schedule_event_submit(request):
    event = request.POST['event']
    place = request.POST['place']
    from_date = request.POST['from']
    to_date = request.POST['to']

    start_date = time.strftime('%Y-%m-%d', time.strptime(from_date, '%m/%d/%Y'))
    end_date = time.strftime('%Y-%m-%d', time.strptime(to_date, '%m/%d/%Y'))

    try:
        # event =
        scheduled_event = Scheduled_Event(
            event_id=event,
            place_id=place,
            start=start_date,
            end=end_date
        )

        scheduled_event.save()

        messages.success(request, 'Your event was sucessfully scheduled.')
    except:
        messages.error(request, 'Unable to schedule your event.')
    return redirect('events:index')

@login_required
def add_place(request):
    name = request.POST['name']
    address = request.POST['address']
    number = request.POST['number']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zip']

    try:
        place = Place(
            name=name,
            street_address=address,
            room_number=number,
            city=city,
            state=state,
            zipcode=zipcode
        )

        place.save()
    except:
        messages.error(request, "There was an error saving the place")
        return redirect('events:index')

    data = {}
    data['events'] = Event.objects.order_by('name').all()
    data['places'] = Place.objects.order_by('name').all()

    return render(request, 'events/schedule_event_form.html', data)

@login_required
def edit_events(request):
    data = {}
    data['events'] = Event.objects.order_by('name').all()

    return render(request, 'events/edit_events_form.html', data)

@login_required
def get_event_info(request):
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)

    data = {}
    data['description'] = event.description
    data['price'] = event.price

    return render(request, 'events/edit_event_info.html', data)
