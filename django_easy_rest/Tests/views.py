from django.views.generic import UpdateView, CreateView

from ..models import TestModel
from .. import views
from ..mixins import DecorativeKeysMixin, HelpMixin, ModelUnpacker, FormPostMixin


class MethodBased(DecorativeKeysMixin, HelpMixin, ModelUnpacker, views.RestApiView):
    method_helpers = {'special_error': {"help": {"general": "this is a special message"}},
                      'super_special': {"help": {"general": "general help",
                                                 "another": "another help"}}}
    api_allowed_methods = ['__all__']

    def correct(self, data):
        return {"test": "test"}

    def error(self, data):
        return 1 / 0

    def special_error(self, data):
        return 1 / 0

    def super_special(self, data):
        return 1 / 0

    def two_parms(self, a, b):
        return {"a---": a, "-b-": b}

    def get_username(self, user):
        return {"username": user.username}

    def test(self, data):
        return {"new action": "test"}

    def new(self, data):
        return {data['username']: "?"}


class UpdateViewApi(FormPostMixin, UpdateView):
    fields = ['name', 'integer']
    template_name = 'django_easy_rest/test.html'
    model = TestModel
    success_message = 'yay'

    def get_object(self, queryset=None):
        return TestModel.objects.get(pk=1)


class CreateViewApi(FormPostMixin, CreateView):
    template_name = 'django_easy_rest/test.html'
    model = TestModel
    fields = ['name', 'integer']
