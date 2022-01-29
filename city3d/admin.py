from django.contrib import admin

from city3d.models import City, State, Building, Permit, Headline

class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "viewport_lat", "viewport_long")

class StateAdmin(admin.ModelAdmin):
    list_display = ( "name", "initials")

class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "gltf", "img", "img_cred", "latitude", "longitude")

class PermitAdmin(admin.ModelAdmin):
    list_display = ("index", "permittype", "permit_number", "permit_class_mapped", "issue_date", "issued_in_last_30_days", "status_current", "expiresdate", "original_address1", "original_city", "original_state", "original_zip", "link", "project_id", "latitude", "longitude", "total_job_valuation")

class HeadlineAdmin(admin.ModelAdmin):
    list_display = ("id", "datetime", "title", "publisher", "link", "img")


admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Permit, PermitAdmin)
admin.site.register(Headline, HeadlineAdmin)
