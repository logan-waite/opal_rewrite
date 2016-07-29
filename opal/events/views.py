from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'events/index.html')

@login_required
def new_event_form(request):
    return render(request, 'events/new_event_form.html')
