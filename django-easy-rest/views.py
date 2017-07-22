from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .utils.search_model import GetModelByString
import json


class MethodApiView(APIView):
    function_field_name = 'action'
    separator = '-'
    general_help_string = ('you can get help by: '
                           '{"{' + function_field_name + '}":"method", "get' + separator + 'help"}'
                                                                                           'for specific help: ',
                           '{"{' + function_field_name + '}":"method", "get' + separator + 'help", "help' + separator + 'prefix":"input [..etc]"}')
    method_helpers = {'__all__': {"help": {"general": "this is a special message"}}}
    api_allowed_methods = ['__all__']

    # this field is responsible of handling model get in functions
    api_handle_models_get = True
    # unpack api data into function
    api_method_packers = True

    # model resolver

    model_resolver = GetModelByString()

    def get(self, serialized_object=None):
        data = {"class": "method view"} if not serialized_object else serialized_object.data
        return Response(data)

    @staticmethod
    def _pythonize(name):
        return name.replace('-', '_').lower()

    # {"action":"error"}
    def post(self, request):
        try:
            if self.function_field_name in request.data:
                action = self._pythonize(request.data[self.function_field_name])
                try:
                    if action not in self.api_allowed_methods and '__all__' not in self.api_allowed_methods:
                        return Response(data={"error": "method not allowed {0}, allowed methods {1}".format(action,
                                                                                                            self.api_allowed_methods)},
                                        status=status.HTTP_403_FORBIDDEN)
                    _method = getattr(self, action)
                    data = request.data
                    output = self._method_wrapper(data, _method, action)
                    if 'out' in output:
                        return Response(data=output['out'], status=status.HTTP_200_OK)
                    else:
                        return Response(data=output, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except (AttributeError, ImportError):
                    return Response(data={"error": "method not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(data={"error": "no method in data"}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, json.JSONDecodeError) as error:
            data = {"error": "general api error"}
            if settings.DEBUG:
                data.update({'debug': {'exception-type': str(type(error)), 'exception-args': error.args}})
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _method_wrapper(self, data, method, action):
        out = None
        additional = None
        try:
            out = method(**self.prepare_function_data(data=data, method=method))
        except Exception as error:
            key = '__all__' if action not in self.method_helpers else action
            if key in self.method_helpers:
                help_prefix = data.get('help' + self.separator + 'prefix', 'general')
                help_message = {"message": self.method_helpers[key]['help'].get(help_prefix, 'help not found'),
                                'usage': 'specific help use {action:' + action + ', help' + self.separator + 'prefix:specific error}',
                                'help' + self.separator + "list": 'available help entries {}'.format(
                                    self.method_helpers[key]['help'].keys())}
                additional = {"help": help_message}
            else:
                additional = {'error': "Exception occurred in method check function usage",
                              self.function_field_name: action}
            if settings.DEBUG:
                additional.update({'debug': {'exception-type': str(type(error)), 'exception-args': error.args}})

        if additional:
            return additional
        if out:
            return {"out": out}
        if settings.DEBUG:
            return {"debug": "method did not return any data"}

    def prepare_function_data(self, data, method=None, append_data=None):
        if append_data is None:
            append_data = {}
        if not method or not self.api_method_packers:
            data = {"data": data}
        else:
            keys = list(method.__code__.co_varnames)
            keys.remove('self')
            if len(keys) == 1:
                data = {keys[0]: data}
            else:
                data = {key: data.get(key, None) for key in keys if
                        key in data}  # if key not in data default parameter ?
        data.update(append_data)
        return data

    def api_abstractions(self, data):
        get_model = 'get{separator}model'.format(separator=self.separator)
        if get_model in data:
            '''
            the get model is as follows:
            
            {"get-model": {"model-name":"User", "query":{"pk":5}, "app":"auth"}}
            
            or 
            
            {"get-model": {"model-name":"auth.User", "query":{"pk":5}}}
            
            default parameter name is lower of model name
            
            '''
            model = self.get_model(**data[get_model])
            del data[get_model]
            data.update(model)
            return data

    def get_model(self, query, field, model_name=None, app=None, split_by='.'):
        if app:
            return {
                model_name.lower(): self.model_resolver.get_model(model_name=model_name, app=app).objetcs.get(**query)}
        else:
            try:
                app, model = field.split(split_by)
                return {model.lower(): self.model_resolver.get_model(model_name=model, app=app).objetcs.get(**query)}
            except ValueError:  # to many or not enough values to unpack
                return None
