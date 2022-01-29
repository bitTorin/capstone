
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("city/<str:city_name>", views.hero, name="hero"),
    path("threebox/<str:city_name>", views.threebox, name="threebox"),
]
