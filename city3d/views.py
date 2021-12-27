from django.shortcuts import render
from django.conf import settings

from .models import City, State

def index(request):

    return render(request, 'city3d/index.html', {
        "cities": City.objects.all().order_by('name')
    })

def hero(request, city_name):
    city = City.objects.get(name = city_name)

    return render( request, 'city3d/city.html', {
        "city": city,
        "cities": City.objects.all().order_by('name')
    })

def test(request):

    return render(request, 'city3d/test.html', {

    })
