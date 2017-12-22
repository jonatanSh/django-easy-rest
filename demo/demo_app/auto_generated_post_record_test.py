from django.test import TestCase
from demo_app.views import ApiTest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from easy_rest.test_framework.resolvers.resolve import register_unitest
from django.test.utils import override_settings

register_unitest()


def resolve_user(pk):
    try:
        return User.objects.get(pk=pk)
    except Exception:
        return AnonymousUser()


