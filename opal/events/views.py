from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event, Place

# Create your views here.
@login_required
def index(request):
    return render(request, 'events/index.html')

@login_required
def new_event_form(request):
    return render(request, 'events/new_event_form.html')

@login_required
def new_event_submit(request):
    name = request.POST['name']
    description = request.POST['description']
    price = request.POST['price']

    print(name)
    print(description)
    print(price)

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
