import calendar, datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request):
    if 'month' in request.POST.keys() and request.POST['month']:
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        # Go back a month
        try:
            if request.POST['prev'] == '1':
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
        except:
            pass
        # Go forward a month
        try:
            print('going next')
            if request.POST['next'] == '1':
                month += 1
                if month > 12:
                    month = 1
                    year += 1
        except:
            pass

    else:
        date = datetime.date
        today = date.today()
        month = today.month
        year = today.year

    calendar = createCalendar(month, year)
    data = {
            'calendar':calendar['calendar'],
            'month':month,
            'month_name':calendar['month_name'],
            'year':year
            }

    return render(request, 'cal/index.html', data)

def createCalendar(month, year):
    newCalendar = calendar.Calendar(6)
    days = newCalendar.monthdatescalendar(year, month)
    calendarDays = {}
    months = calendar.month_name

    i = 0
    for x in days:
        calendarDays[i] = x
        i += 1

    returnedCalendar = {'calendar':calendarDays, 'month_name':months[month]}
    return returnedCalendar
