from django.contrib import admin

from .models import City, State

class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")

class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "initials")

# class PermitAdmin(admin.ModelAdmin):
#     list_display = ("active_status", "issued_date", "last30days", "expires_date", "address", "zip_code", "city_project_id")


admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
# admin.site.register(BuildingPermits, PermitAdmin)
