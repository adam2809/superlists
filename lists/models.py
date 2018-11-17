from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    name = models.TextField(default='')
    daysAhead = models.TextField(default='')
    time = models.TextField(default='')
    list = models.ForeignKey(List,default=None,on_delete=models.CASCADE)
