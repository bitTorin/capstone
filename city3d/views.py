from django.shortcuts import render
from django.http import JsonResponse
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
        "cities": City.objects.all().order_by('name'),
    })

def test(request):

    return render(request, 'city3d/test.html', {

    })

def three(request):

    return render(request, 'city3d/three.html', {

    })

def add(request):

    return render(request, 'city3d/add.html', {

    })

def maps(request):

    return render(request, 'city3d/maps.html', {
        "maps_api": settings.MAPS_API,
    })

def mapbox(request):

    return render(request, 'city3d/mapbox.html', {

    })

def maplibre(request):

    return render(request, 'city3d/maplibre.html', {

    })
