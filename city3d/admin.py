from django.contrib import admin

from city3d.models import City, State, Building, Permit, Headline

class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "viewport_lat", "viewport_long")

class StateAdmin(admin.ModelAdmin):
    list_display = ( "name", "initials")

class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "gltf", "img", "img_cred", "latitude", "longitude")

class PermitAdmin(admin.ModelAdmin):
    list_display = ("index", "permit_type", "permit_number", "permit_class", "project_id", "issue_date", "last_30_days", "current_status", "expires_date", "address", "city", "state", "zip", "link", "latitude", "longitude", "valuation")

class HeadlineAdmin(admin.ModelAdmin):
    list_display = ("id", "datetime", "title", "publisher", "link", "img")


admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Permit, PermitAdmin)
admin.site.register(Headline, HeadlineAdmin)
