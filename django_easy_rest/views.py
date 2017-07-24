from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .utils.search_model import GetModelByString
from .serializers import FullDebuggerSerializer
import json
from copy import copy


class FullMethodApiView(APIView):
    function_field_name = 'action'
    separator = '-'
    general_help_string = ('you can get help by: '
                           '{"{' + function_field_name + '}":"' + function_field_name + '", "get' + separator + 'help"}'
                                                                                                                'for specific help: ',
                           '{"{' + function_field_name + '}":"' + function_field_name + '", "get' + separator + 'help", "help' + separator + 'prefix":"input [..etc]"}')
    method_helpers = {'__all__': {"help": {"general": "this is a special message"}}}
    api_allowed_methods = ['__all__']

    api_abstraction_methods = ['__all__']

    # model resolver

    model_resolver = GetModelByString()

    debug_serializer = FullDebuggerSerializer()

    def get(self, serialized_object=None):
        data = {"class": "method view"} if not serialized_object else serialized_object.data
        return Response(data)

    @staticmethod
    def _pythonize(name):
        return name.replace('-', '_').lower()

    def restifiy(self, data):
        if ' ' in data:
            return data.replace(' ', self.separator)
        if '_' in data:
            return data.replace('_', self.separator)
        if '-' in data:
            return data.replace('-', self.separator)

    # {"action":"error"}
    def post(self, request):
        base_response = {}
        if settings.DEBUG:
            base_response['debug'] = {self.restifiy("api attributes"):
                                          {self.restifiy("api allowed methods"): self.api_allowed_methods,
                                           self.restifiy("api abstraction methods"): self.api_abstraction_methods}}
        try:
            data, debug_data = self.api_abstractions(request.data)
            if settings.DEBUG:
                base_response["debug"]["processed-data"] = debug_data
            if self.function_field_name in data:
                action = self._pythonize(data[self.function_field_name])
                try:
                    if action not in self.api_allowed_methods and '__all__' not in self.api_allowed_methods:
                        base_response['error'] = '{0} {1} not allowed , allowed {0} {2}'.format(
                            self.function_field_name,
                            action,
                            self.api_allowed_methods)
                        return Response(data=base_response,
                                        status=status.HTTP_403_FORBIDDEN)
                    _method = getattr(self, action)
                    output, debug = self._method_wrapper(data, _method, action)
                    base_response['debug'].update(debug)
                    if 'out' in output:
                        base_response['data'] = output['out']
                        return Response(data=base_response, status=status.HTTP_200_OK)
                    else:
                        base_response['data'] = output
                        return Response(data=base_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except (AttributeError, ImportError) as error:
                    base_response['error'] = "{} not found".format(self.function_field_name)
                    base_response['debug'].update({"exception": str(error)})
                    return Response(data=base_response, status=status.HTTP_404_NOT_FOUND)
            base_response['error'] = "no {} in data".format(self.function_field_name)
            return Response(data=base_response, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, json.JSONDecodeError) as error:
            base_response["error"] = "general api error"
            if settings.DEBUG:
                base_response['debug'].update({'exception-type': str(type(error)), 'exception-args': error.args})
            return Response(data=base_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _method_wrapper(self, data, method, action):
        out = None
        additional = None
        debug = {}
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
                debug = {'exception-type': str(type(error)), 'exception-args': error.args}

        if additional:
            return additional, debug
        if out:
            return {"out": out}, debug
        if settings.DEBUG:
            return {}, {"error": '{} did not return any data'.format(self.function_field_name)}

    def prepare_function_data(self, data, method=None, append_data=None):
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

    def api_abstractions(self, data):
        debug_data = copy(data)
        check = lambda item: True
        if '__all__' not in self.api_abstraction_methods:
            check = lambda item: self._pythonize(item) in self.api_abstraction_methods

        if check("get model"):
            get_model_key = self.restifiy('get model')
            if get_model_key in data:
                data, debug_data = self.handle_get_model(data=data, get_model=get_model_key, debug_data=debug_data)
        return data, debug_data

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
