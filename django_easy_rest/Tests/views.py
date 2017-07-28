from django.views.generic import UpdateView, CreateView
from datetime import datetime
from django.contrib.auth.models import User
from .. import views
from ..mixins import DecorativeKeysMixin, HelpMixin, ModelUnpacker, FormPostMixin


class MethodBased(DecorativeKeysMixin, HelpMixin, ModelUnpacker, views.RestApiView):
    method_helpers = {'special_error': {"help": {"general": "this is a special message"}},
                      'super_special': {"help": {"general": "general help",
                                                 "another": "another help"}}}
    api_allowed_methods = ['__all__']

    @staticmethod
    def echo(data):
        return data

    @staticmethod
    def error(data):
        return 1 / 0

    @staticmethod
    def special_error(data):
        return 1 / 0

    @staticmethod
    def super_special(data):
        return 1 / 0

    @staticmethod
    def two_parms(a, b):
        return {"a---": a, "-b-": b}

    @staticmethod
    def get_username(user):
        return {"username": user.username}

    @staticmethod
    def test(data):
        return {"new action": "test"}

    @staticmethod
    def new(data):
        return {data['username']: "?"}


class UpdateViewApi(FormPostMixin, UpdateView):
    fields = ['first_name', 'last_name']
    template_name = 'django_easy_rest/test.html'
    model = User
    success_message = 'model has been changed {}'.format(datetime.now())

    def get_object(self, queryset=None):
        return User.objects.get(pk=1)


class CreateViewApi(FormPostMixin, CreateView):
    template_name = 'django_easy_rest/test.html'
    model = User
    fields = ['username', 'email', 'password']
    success_message = 'user created {}'.format(datetime.now())
