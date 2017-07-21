from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .decorators import _ApiMethod


class MethodApiView(object):
    function_field_name = 'action'
    separator = '-'
    general_help_string = ('you can get help by: '
                           '{"{' + function_field_name + '}":"method", "get' + separator + 'help"}'
                                                                                           'for specific help: ',
                           '{"{' + function_field_name + '}":"method", "get' + separator + 'help", "help' + separator + 'prefix":"input [..etc]"}')

    def get(self, serialized_object=None):
        data = {"class": "method view"} if not serialized_object else serialized_object.data
        return Response(data)

    @staticmethod
    def _pythonize(name):
        return name.replace('-', '_').lower()

    def post(self, request):
        if self.function_field_name in request.data:
            action = self._pythonize(request.data[self.function_field_name])
            try:
                _method = getattr(self, action)
                try:
                    data = request.data
                    if type(_method) is type(_ApiMethod):
                        return Response(_method.__call__(data), status=status.HTTP_200_OK)
                    else:
                        return Response(_method(data), status=status.HTTP_200_OK)
                except Exception as e:
                    data = {'error': "Exception occurred in method check function usage",
                            'action': self.function_field_name}
                    if type(_method) is type(_ApiMethod):
                        help_prefix = request.data.get('help' + self.separator + 'prefix', 'general')
                        data = _method.get_help(prefix=help_prefix)
                    if settings.DEBUG:
                        data.update({'debug': {'exception-type': type(e), 'exception-args': e.args}})
                    return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except (AttributeError, ImportError):
                return Response(data={"error": "method not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"error": "no method in data"}, status=status.HTTP_400_BAD_REQUEST)
