from django.contrib import admin

# Register your models here.
from django_easy_rest.models import TestModel

admin.site.register(TestModel)