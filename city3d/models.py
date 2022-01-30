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
        db_table = "cities"

    def __str__(self):
        return f"{self.name}"

class State(models.Model):
    name = models.CharField(max_length=64)
    initials = models.CharField(primary_key=True, max_length=2)

    class Meta:
        db_table = "states"

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

    class Meta:
        db_table = "buildings"

    def __str__(self):
        return f"{self.name}"

class Headline(models.Model):
    datetime = models.DateTimeField(null=True)
    title = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    link = models.URLField()
    img = models.URLField()

    class Meta:
        db_table = "headlines"

    def __str__(self):
        return f"{self.title}"

class Permit(models.Model):
    index = models.IntegerField(primary_key=True)
    permit_type = models.CharField(max_length=20)
    permit_number = models.CharField(max_length=20)
    permit_class = models.CharField(max_length=20)
    project_id = models.IntegerField()
    issue_date = models.DateTimeField()
    last_30_days = models.CharField(max_length=3)
    current_status = models.CharField(max_length=20)
    expires_date = models.DateTimeField()
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip = models.IntegerField()
    link = models.URLField()
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, blank=True)
    valuation = models.FloatField()

    class Meta:
        db_table = "permits"

    def __str__(self):
        return f"{self.id}"
