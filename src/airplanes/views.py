from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpRequest, response
from . models import Flat

AIRPORTS = {"ATL":"Hartsfield Atlanta International",
    "BWI":"Washington DC - Baltimore Washington International",
    "DFW":"Dallas/Fort Worth International" ,
    "JFK":"New York - John F. Kennedy",
    "LAX":"Los Angeles",
    "ORD":"Chicago - O'Hare International",
    "SFO":"San Francisco",
};

def code_to_airport(request, airport):
    airport = AIRPORTS.get(airport.upper(), 'airport code is not found')
    ctx = {
        'code' : airport
    }
    return render(request, template_name ='airport_code.html', context=ctx)


def homepage(request):
    return render(request, template_name='homepage.html', context={})

def flat_detail(request, flat_id):
    flat = Flat.objects.get(pk=flat_id)
    ctx = {
        'flat' : flat
    }
    return render(request, template_name='flat.html', context=ctx)

def flat_list(request):
    flat_list = Flat.objects.all()
    ctx = {
        'flat_list' : flat_list
    }
    return render(request, template_name='flat_list.html', context=ctx)

