from easy_rest.views import RestApiView
from easy_rest.mixins import ModelUnpacker, FunctionUnPackerMixin, DecorativeKeysMixin, HelpMixin, FormPostMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.models import User
from easy_rest.test_framework.recorder.post_record_mixins import PostRecordTestGenerator


class ApiTest(ModelUnpacker, FunctionUnPackerMixin, DecorativeKeysMixin, HelpMixin,
              '''PostRecordTestGenerator''', RestApiView):
    get_data = {"purpose": "this is a demo for the easy rest framework",
                "usage": {'echo': {"description": "echos back any information use echo",
                                   "usage": '{"action":"echo","data":"any-data"}'}},
                'get_username': {"description": "returns the username of the requested user",
                                 "usage": '{"action":"get_username", "with-model": {"field":"auth.User", "query":{'
                                          '"pk":1}}}'}
                }git 

    # def __init__(self, *args, **kwargs):
    #     super(ApiTest, self).__init__(*args, **kwargs)
    #     self.init_test(app_name='demo_app')

    def echo(self, data):
        return {"echo": data}

    @staticmethod
    def get_username(user):
        return {"username": user.username}


class RestUpdate(FormPostMixin, UpdateView):
    template_name = "demo_app/base.html"
    fields = ['first_name', 'last_name']
    model = User
    success_message = 'details updated successfully'

    def get_object(self, queryset=None):
        return User.objects.get(pk=1)


class RestCreate(FormPostMixin, CreateView):
    fields = ['username', 'password']
    template_name = "demo_app/base.html"
    model = User
    success_message = 'created user successfully'


class WelcomePage(TemplateView):
    template_name = 'demo_app/home.html'
