from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.files.storage import FileSystemStorage
from datetime import datetime

gltf_path = FileSystemStorage(location='/static/city3d/buildings/austin/gltf')
img_path = FileSystemStorage(location='/static/city3d/buildings/austin/img')

class City(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    # state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    viewport_lat = models.DecimalField(max_digits = 8, decimal_places = 6, blank=True)
    viewport_long = models.DecimalField(max_digits = 9, decimal_places = 6, blank=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}"

class State(models.Model):
    name = models.CharField(max_length=64)
    initials = models.CharField(primary_key=True, max_length=2)

    class Meta:
        db_table = "city3d_state"

    def __str__(self):
        return f"{self.initials}"

class Building(models.Model):
    name = models.CharField(max_length=64)
    gltf = models.FileField(storage=gltf_path)
    img = models.FileField(storage=img_path)
    img_cred = models.CharField(max_length=64, default='', blank=True)
    address = models.CharField(max_length=64)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    model_rotation = models.DecimalField(max_digits = 5, decimal_places = 2, default=0, null=True)


    def __str__(self):
        return f"{self.name}"

class Headline(models.Model):
    datetime = models.DateTimeField(null=True)
    title = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    link = models.URLField()
    img = models.URLField()

    def __str__(self):
        return f"{self.title}"

class Permit(models.Model):
    index = models.IntegerField(primary_key=True)
    permittype = models.CharField(max_length=20)
    permit_number = models.CharField(max_length=20)
    permit_class_mapped = models.CharField(max_length=20)
    issue_date = models.DateTimeField()
    issued_in_last_30_days = models.CharField(max_length=3)
    status_current = models.CharField(max_length=20)
    expiresdate = models.DateTimeField()
    original_address1 = models.CharField(max_length=64)
    original_city = models.CharField(max_length=64)
    original_state = models.CharField(max_length=64)
    original_zip = models.IntegerField()
    link = models.URLField()
    project_id = models.IntegerField()
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    total_job_valuation = models.FloatField()

    class Meta:
        db_table = "city3d_permit"

    def __str__(self):
        return f"{self.id}"
