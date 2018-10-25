from django.db import models

class Item(models.Model):
    name = models.TextField(default='')
    daysAhead = models.IntegerField(default=0)
    time = models.TextField(default='')
