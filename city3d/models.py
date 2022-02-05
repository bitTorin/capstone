import os
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class City(models.Model):
    name = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    viewport_lat = models.DecimalField(max_digits = 8, decimal_places = 6, blank=True)
    viewport_long = models.DecimalField(max_digits = 9, decimal_places = 6, blank=True)

    class Meta:
        verbose_name_plural = "cities"
        db_table = "cities"

    def __str__(self):
        return f"{self.name}"

class Building(models.Model):
    name = models.CharField(max_length=64)
    img = models.FileField(storage=MyStorage())
    img_cred = models.CharField(max_length=64, default='', blank=True)
    address = models.CharField(max_length=64)
    latitude = models.DecimalField(max_digits = 20, decimal_places = 17, blank=True)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 17, blank=True)
    model_rotation = models.DecimalField(max_digits = 5, decimal_places = 2, default=0, null=True)
    developer = models.CharField(max_length=64, default='', blank=True)
    contractor = models.CharField(max_length=64, default='', blank=True)
    architect = models.CharField(max_length=64, default='', blank=True)
    permit = models.ForeignKey('Permit', on_delete=models.PROTECT, null=True, blank=True, related_name="permits")
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, blank=True)

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
    building = models.ForeignKey('Building', on_delete=models.PROTECT, null=True, blank=True, related_name="headlines")

    class Meta:
        db_table = "headlines"

    def __str__(self):
        return f"{self.title}"

class Permit(models.Model):
    permit_type = models.CharField(max_length=20)
    permit_number = models.CharField(max_length=20)
    permit_class = models.CharField(max_length=20)
    project_id = models.CharField(max_length=20)
    issue_date = models.DateTimeField(null=True, blank=True)
    last_30_days = models.CharField(max_length=3)
    current_status = models.CharField(max_length=20)
    expires_date = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip = models.IntegerField()
    link = models.URLField()
    latitude = models.DecimalField(max_digits = 20, decimal_places = 17, blank=True)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 17, blank=True)
    valuation = models.DecimalField(max_digits = 20, decimal_places = 2, default=0.00)
    building = models.ForeignKey('Building', on_delete=models.PROTECT, null=True, blank=True, related_name="buildings")

    class Meta:
        db_table = "permits"

    def __str__(self):
        return f"{self.permit_number}"
