from django.db import models


class State(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
# Create your models here.
