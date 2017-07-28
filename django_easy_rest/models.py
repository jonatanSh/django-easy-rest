from django.db import models


class TestModel(models.Model):
    integer = models.IntegerField(default=2)

    name = models.CharField(max_length=44, default="name")
