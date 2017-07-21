from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
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
            out = method(data)
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
