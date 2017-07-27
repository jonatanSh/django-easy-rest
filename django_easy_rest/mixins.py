from copy import copy

from django.conf import settings
from django.http import HttpResponse

from django_easy_rest.serializers import FullDebuggerSerializer
from django_easy_rest.utils.search_model import GetModelByString
from django.views.decorators.csrf import csrf_exempt
import json


class FunctionUnPackerMixin(object):
    """
    This mixin handles the unpacking of variables into functions

    Example: unpacks {'a':'value of a', 'b':'value of b'} results in function(a='value of a', b='value of b')
    """

    @staticmethod
    def prepare_function_data(data, method=None, append_data=None):
        prepared_data = {}
        if append_data is None:
            append_data = {}
        if not method:
            prepared_data = {"data": data}
        else:
            keys = list(method.__code__.co_varnames)
            if 'self' in keys:
                keys.remove('self')
            if not keys:
                keys = []
            unpacked = False
            for key in keys:
                if key in data:
                    unpacked = True
                    prepared_data[key] = data[key]
            if not unpacked:
                prepared_data = {keys[0]: data}
        prepared_data.update(append_data)
        return prepared_data

    def call_method(self, data, method):
        return method(**self.prepare_function_data(data=data, method=method, append_data=None))


class HelpMixin(object):
    """
    All fields initialized after inheritance
    """
    general_help_string = 'for function summary use: {usage}'
    method_helpers = {'__all__': {"help": {"general": "this is a special message"}}}

    def __init__(self, *args, **kwargs):
        self.general_help_string.format(usage=self.get_general_function_help_usage())

    def get_general_function_help_usage(self, action=None):
        if not action:
            action = "specific" + self.function_field_name
        help_prefix_string = self.restifiy('help prefix')
        return {self.function_field_name: action, help_prefix_string: "specific error"}

    def _method_wrapper(self, data, method, action):
        """

        :param data: request.data (dict)
        :param method: method to call inside api (object)
        :param action: action name (str)
        :return: function data, debug, error [type = Bool]
        """
        out = None
        additional = None
        debug = {}
        try:
            out = self.call_method(data=data, method=method)
        except Exception as error:
            key = '__all__' if action not in self.method_helpers else action
            if key in self.method_helpers:
                help_prefix_string = self.restifiy('help prefix')
                help_prefix = data.get(help_prefix_string, 'general')
                help_message = {"message": self.method_helpers[key]['help'].get(help_prefix, 'help not found'),
                                'usage': 'specific help use {usage}'.format(
                                    usage=self.get_general_function_help_usage(action=action)),
                                self.restifiy('help list'): 'available help entries {helpers}'.format(
                                    helpers=self.method_helpers[key]['help'].keys())}

                additional = {"help": help_message}
            else:
                additional = {'error': "Exception occurred in method check function usage",
                              self.function_field_name: action}
            if settings.DEBUG:
                debug = {'exception-type': str(type(error)), 'exception-args': error.args}

        if additional:
            return additional, debug, True
        if out:
            return out, debug, False
        if settings.DEBUG:
            return {}, {"error": '{} did not return any data'.format(self.function_field_name)}, True


class DecorativeKeys(object):
    separator = '-'

    decorative_keys_formats = [' ', "-", ":"]

    def _pythonize(self, name):
        """
        make action/method name into python friendly variable.
        :param name:
        :return:
        """
        for value in self.decorative_keys_formats:
            name = name.replace(value, "_")
        if self.separator in name:
            name = name.replace(self.separator, '_')
        return name.lower()

    def restifiy(self, data):
        """
        Created a rest item key.
        :param data:
        :return:
        """
        for value in self.decorative_keys_formats:
            return data.replace(value, self.separator)
        if '_' in data:
            return data.replace('_', self.separator)


class ModelUnpacker(FunctionUnPackerMixin):
    api_abstraction_methods = ['__all__']

    # model resolver

    model_resolver = GetModelByString()

    debug_serializer = FullDebuggerSerializer()

    def api_abstractions(self, data):
        debug_data = copy(data)
        check = lambda item: True
        if '__all__' not in self.api_abstraction_methods:
            check = lambda item: self._pythonize(item) in self.api_abstraction_methods

        if check("get model"):
            get_model_key = self.restifiy('get model')
            if get_model_key in data:
                data, debug_data = self.handle_get_model(data=data, get_model=get_model_key, debug_data=debug_data)

        self.base_response['debug'][self.restifiy('processed data')] = debug_data
        return data

    def handle_get_model(self, data, get_model, debug_data):
        if type(data[get_model]) is not list:
            data[get_model] = [data[get_model]]
        for i in range(len(data[get_model])):
            obj, debug_obj = self.get_model(**data[get_model][i])
            prm_key = list(obj.keys())[0]
            if prm_key in data:
                data[prm_key] = [data[prm_key], obj[prm_key]]
                debug_data[prm_key] = [debug_data[prm_key], debug_obj[prm_key]]
            else:
                data.update(obj)
                debug_data.update(debug_obj)
        del data[get_model]
        del debug_data[get_model]
        return data, debug_data

    def get_model(self, query, field=None, model_name=None, app=None, split_by='.', name=None):
        if app:
            model = self.model_resolver.get_model(model_name=model_name, app=app).objects.get(**query)
            if not name:
                name = model_name.lower()
            return {name: model}, {name: self.debug_serializer.serialize(model)}
        else:
            try:
                app, model = field.split(split_by)
                return self.get_model(query=query, app=app, model_name=model, split_by=split_by, name=name)
            except ValueError:  # to many or not enough values to unpack
                return None, None


class FormPostMixin(object):
    """
    this mixin supports django GCBV and make posts using a rest api
    """

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}
        form = self.get_form()
        self.object = self.get_object()
        print(form.__dict__)
        if form.is_valid():
            response = {"status": "post-success"}
        else:
            response = {"status": "post-failure",
                        "form_cleaned_data": form.cleaned_data,
                        "form_errors": form.errors}
        return HttpResponse(json.dumps(response))
