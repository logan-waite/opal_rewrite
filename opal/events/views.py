import time
import sys

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from events.models import Event, Place, Scheduled_Event, Checklist_Item, Scheduled_Event_Checklist

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

        # get checklist items for scheduled event
        checklist_items = Scheduled_Event_Checklist.objects.all().filter(scheduled_event=event.id)
        event.items = checklist_items

        completed = True     # Assume true until proven wrong
        for item in checklist_items:
            if not item.completed:
                completed = False

        event.completed = completed
    data['events'] = scheduled_events

    return render(request, 'events/index.html', data)

@login_required
def new_event_form(request):
    data = {}
    all_checklist_items = Checklist_Item.objects.all()
    data['checklist'] = all_checklist_items

    return render(request, 'events/new_event_form.html', data)

@login_required
def new_event_submit(request):
    checked_checklist_items = request.POST.getlist('checklist_items')
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

        for item in checked_checklist_items:
            event.checklist_items.add(item)

        messages.success(request, "Your event was saved successfully.")
    except:
        e = sys.exc_info()[0]
        messages.error(request, "There was an error saving your event.")
        print(e)

    return redirect('events:index')

@login_required
def schedule_event_form(request):
    data = {}
    data['events'] = Event.objects.order_by('name').all()
    data['places'] = Place.objects.order_by('name').all()

    return render(request, 'events/schedule_event_form.html', data)

@login_required
def schedule_event_submit(request):
    event_id = request.POST['event']
    place = request.POST['place']
    from_date = request.POST['from']
    to_date = request.POST['to']

    # format date strings for database
    start_date = time.strftime('%Y-%m-%d', time.strptime(from_date, '%m/%d/%Y'))
    end_date = time.strftime('%Y-%m-%d', time.strptime(to_date, '%m/%d/%Y'))

    try:
        scheduled_event = Scheduled_Event(
            event_id=event_id,
            place_id=place,
            start=start_date,
            end=end_date
        )

        scheduled_event.save()

        # set up checklist items for checking off.
        event = Event.objects.get(pk=event_id)
        checklist_items = event.checklist_items.all()
        print(checklist_items)
        for item in checklist_items:
            scheduled_checklist = Scheduled_Event_Checklist (
                scheduled_event = scheduled_event,
                checklist_item = item,
                completed = 0
            )
            scheduled_checklist.save()

        messages.success(request, 'Your event was sucessfully scheduled.')
    except:
        e = sys.exc_info()
        print(e)
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
    data = {}

    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    all_checklist_items = Checklist_Item.objects.all()
    checked_checklist = []
    for item in event.checklist_items.all():
        checked_checklist.append(item)
        data['checked_checklist'] = checked_checklist

    data['name'] = event.name
    data['description'] = event.description
    data['price'] = event.price
    data['event_id'] = event_id
    data['checklist'] = all_checklist_items

    return render(request, 'events/edit_event_info.html', data)

@login_required
def new_checklist_item(request):
    checklist_item = request.POST['checklist_item']

    try:
        item = Checklist_Item(
            name=checklist_item
        )
        item.save()
    except:
        messages.error(request, "There was an error saving your checklist item")
        return redirect('events:index')

    if request.POST['event_id'] == 'new':
        return new_event_form(request)
    else:
        return get_event_info(request)

@login_required
def edit_event_submit(request):
    checked_checklist_items = request.POST.getlist('checklist_items')
    event_id = request.POST['event']
    description = request.POST['description']
    price = request.POST['price']
    name = request.POST['name']
    try:
        event = Event.objects.get(pk=event_id)
        event.description = description
        event.price = price
        event.name = name

        event.checklist_items.clear()
        for item in checked_checklist_items:
            event.checklist_items.add(item)

        event.save()

        # Get scheduled event to update their checklist items
        scheduled_events = Scheduled_Event.objects.filter(event=event).all()
        for event in scheduled_events:
            scheduled_event_checklist = Scheduled_Event_Checklist.objects.filter(scheduled_event=event).all()
            checklist = {}
            for item in scheduled_event_checklist:
                # Save old checklist
                checklist[item.checklist_item.name] = item.completed
                item.delete()
            # Create new checklist items
            for item in checked_checklist_items:
                checklist_item = Checklist_Item.objects.get(pk=item)
                print(checklist)
                print(checklist_item.name)
                if checklist_item.name in checklist:
                    completed = checklist[checklist_item.name]
                    # if checklist[checklist_item.name] == True:
                    #     completed = 1
                    # else:
                    #     completed = 0
                else:
                    completed = 0

                scheduled_checklist = Scheduled_Event_Checklist (
                    scheduled_event = event,
                    checklist_item = checklist_item,
                    completed = completed
                )
                scheduled_checklist.save()
        messages.success(request, "Event successfully changed")
    except:
        e = sys.exc_info()
        print(e)
        messages.error(request, "An error occurred when editing your event")

    return redirect('events:index')

@login_required
def save_item_status(request):
    checked = request.POST['checked']
    item_id = request.POST['item_id']
    if(checked == '1'):
        completed = True
    else:
        completed = False

    try:
        checklist_item = Scheduled_Event_Checklist.objects.get(pk=item_id)
        checklist_item.completed = completed

        checklist_item.save()

        # Check if entire checklist is complete
        checklist = Scheduled_Event_Checklist.objects.filter(scheduled_event=checklist_item.scheduled_event)
        completed = True     # Assume true until proven wrong
        for item in checklist:
            if not item.completed:
                completed = False
        if (completed):
            return HttpResponse("complete")
        else:
            return HttpResponse("incomplete")
    except:
        e = sys.exc_info()
        print(e)

        return HttpResponse(e)
