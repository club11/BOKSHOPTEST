from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpRequest, response

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