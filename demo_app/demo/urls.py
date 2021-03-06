"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from demo_app.views import ApiTest, RestUpdate, RestCreate, WelcomePage, ActiveTemplate, Error

# this will auto realod the app for any change in easy_rest app

urlpatterns = [
    url(r'^update/', RestUpdate.as_view(), name='update-view'),
    url(r'^active_ctx/', ActiveTemplate.as_view(), name='active-ctx'),
    url(r'^error/', Error.as_view()),

    url(r'^create/', RestCreate.as_view(), name='create-view'),
    url(r'^$', WelcomePage.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^easy_rest/', include('easy_rest.urls'), name='rest_urls'),
]

urlpatterns += format_suffix_patterns([
    url(r'api/', ApiTest.as_view(), name='api-view'),
])
