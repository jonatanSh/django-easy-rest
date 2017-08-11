from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .Tests import views

from django.contrib import staticfiles

urlpatterns = [
    url(r'^api/', views.MethodBased.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) + [

    url(r'^update', views.UpdateViewApi.as_view()),
    url(r'^create', views.CreateViewApi.as_view()),

]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', staticfiles.views.serve),
]
