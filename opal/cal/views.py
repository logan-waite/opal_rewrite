import calendar
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    calendar = createCalendar()
    return render(request, 'cal/index.html', calendar)

def createCalendar():
    newCalendar = calendar.HTMLCalendar()
    return newCalendar.formatmonth(2016, 7)
