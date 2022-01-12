
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("city/<str:city_name>", views.hero, name="hero"),
    path("test", views.test, name="test"),
    path("three", views.three, name="three"),
    path("add", views.add, name="add"),
    path("maps", views.maps, name="maps"),
    path("mapbox", views.mapbox, name="mapbox"),
]
