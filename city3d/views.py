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
        "token": settings.CESIUM,
    })

def test(request):

    return render(request, 'city3d/test.html', {
        "token": settings.CESIUM,
    })

def three(request):

    return render(request, 'city3d/three.html', {
        "token": settings.CESIUM,
    })

def add(request):

    return render(request, 'city3d/add.html', {
        "token": settings.CESIUM,
    })
