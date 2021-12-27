from django.db import models
from django.db.models.fields.related import ForeignKey

class City(models.Model):
    name = models.CharField(max_length=64)
    state = models.ForeignKey(State)
