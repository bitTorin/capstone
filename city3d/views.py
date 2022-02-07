from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from .models import City, Building, Permit, Headline

def index(request):

    return render(request, 'city3d/index.html', {
        "cities": City.objects.all().order_by('name'),
        "token": settings.MAPBOX_API,
    })


def hero(request, city_name):
    city = City.objects.get(name = city_name)

    return render( request, 'city3d/city.html', {
        "city": city,
        "cities": City.objects.all().order_by('name'),
        "token": settings.MAPBOX_API,
        "buildings": Building.objects.all(),
        "permits": Permit.objects.filter(city=city),
        "headlines": Headline.objects.all().order_by('-datetime')
    })
