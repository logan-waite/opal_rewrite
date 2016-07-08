import calendar
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request):
    calendar = createCalendar()
    data = {'calendar':calendar}
    data['month'] = 7
    return render(request, 'cal/index.html', data)

def createCalendar():
    newCalendar = calendar.Calendar()
    days = newCalendar.monthdatescalendar(2016, 7)
    calendarDays = {}
    i = 0

    for x in days:
        calendarDays[i] = x
        i += 1

    return calendarDays
