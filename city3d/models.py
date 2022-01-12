from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='/static/city3d/buildings/austin/gltf')

class City(models.Model):
    name = models.CharField(max_length=64)
    state = models.ForeignKey('State', on_delete=models.CASCADE, related_name='state')
    latitude = models.DecimalField(max_digits = 8, decimal_places = 6, blank=True)
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places = 0, blank=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}, {self.state.initials}"

class State(models.Model):
    name = models.CharField(max_length=64)
    initials = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.initials}"

class Buildings(models.Model):
    file = models.FileField(storage=fs)
    latitude = models.DecimalField(max_digits = 8, decimal_places = 6, blank=True)
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6, blank=True)
    drawing_url = models.URLField(max_length = 200)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='city')


# class BuildingPermits(models.Model):
#     type = models.CharField(max_length=12)
#     active_status = models.BooleanField(default=True)
#     issued_date = models.DateTimeField()
#     expires_date = models.DateTimeField()
#     address = models.CharField(max_length=64)
#     zip_code = models.IntegerField()
#     city_project_id = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.id}"

# class Permits(models.Model):
#     permit_type_desc =
#     permit_class_mapped =
#     issue_date =
#     issued_in_last_30_days =
#     status_current =
#     expiresdate =
#     original_address1 =
#     original_city =
#     original_state =
#     original_zip =
#     link =
#     project_id =
#     latitude =
#     longitude =
#
#     def __str__(self):
#         return f"{self.id}"
