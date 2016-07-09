import calendar, datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request):
    if 'month' in request.POST.keys() and request.POST['month']:
        month = int(request.POST['month'])
        if request.POST['direction'] == 'prev':
            month -= 1
        elif request.POST['direction'] == 'next':
            month += 1
        print (month)
        year = 2016
        calendar = createCalendar(month, year)
        data = {'calendar':calendar, 'month':month}
        return render(request, 'cal/calendar.html', data)
    else:
        date = datetime.date
        today = date.today()
        month = today.month
    year = 2016
    calendar = createCalendar(month, year)
    data = {'calendar':calendar, 'month':month}
    return render(request, 'cal/index.html', data)

def createCalendar(month, year):
    newCalendar = calendar.Calendar()
    days = newCalendar.monthdatescalendar(year, month)
    calendarDays = {}
    i = 0

    for x in days:
        calendarDays[i] = x
        i += 1

    return calendarDays
