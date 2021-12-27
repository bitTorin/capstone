from django.contrib import admin

from .models import City, State

class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")

class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "initials")

admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
