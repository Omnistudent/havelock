from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event
import random

def grid(request):
    grid_size = 20
    square_size = 30
    squares = [(i, j) for i in range(grid_size) for j in range(grid_size)]
    return render(request, 'event/grid.html', {'squares': squares, 'square_size': square_size})   



    
     

def all_events(request):
    event_list=Event.objects.all()
    return render(request,'event/event_list.html',
        {'event_list':event_list})


def home(request,year=datetime.now().year,month="March"):
    name="Theo"
    month=month.title()
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    cal=HTMLCalendar().formatmonth(
        year,
        month_number)

    #now=datetime.now()
    #current_year=now.year

    return render(request,
    'event/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
    })