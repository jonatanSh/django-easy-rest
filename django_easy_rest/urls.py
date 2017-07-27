from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .Tests import views

urlpatterns = [
    url(r'^test/', views.MethodBased.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) + [

    url(r'^$', views.UpdateViewApi.as_view())
]
