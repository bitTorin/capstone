from django.db import models
from django.db.models.fields.related import ForeignKey

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
