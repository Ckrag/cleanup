from django.contrib.auth.models import User
from django.db import models


class CleanRoute(models.Model):
    indexes = [
        models.Index(fields=['author']),
        models.Index(fields=['pub_date']),
        models.Index(fields=['decay_date']),
    ]
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    decay_date = models.DateTimeField('date decayed')
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()


class CleanNode(models.Model):
    indexes = [
        models.Index(fields=['lat']),
        models.Index(fields=['lng']),
        models.Index(fields=['author']),
        models.Index(fields=['pub_date']),
        models.Index(fields=['decay_date']),
    ]
    lat = models.FloatField()
    lng = models.FloatField()

    decay_date = models.DateTimeField('date decayed')

    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(CleanRoute, on_delete=models.CASCADE)

    objects = models.Manager()
