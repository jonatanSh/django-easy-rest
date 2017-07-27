from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import json


class RestApiView(APIView):
    """
    Method based api view
    """
    function_field_name = 'action'
    api_allowed_methods = ['__all__']

    get_data = {}

    # initial value
    base_response = None

    def get(self, reuqest):
        if type(self.get_data) is not dict or type(self.get_data) is not str:
            self.get_data = {}
        return Response(self.get_data)

    def _pythonize(self, name):
        return name.lower()

    def restifiy(self, data):
        return data

    def post(self, request):
        self.base_response = self.create_base_response()
        try:
            data = self.api_abstractions(request.data)
            print(data)
            if self.function_field_name in data:
                action = self._pythonize(data[self.function_field_name])
                try:
                    if action not in self.api_allowed_methods and '__all__' not in self.api_allowed_methods:
                        self.base_response['error'] = '{0} {1} not allowed , allowed {0} {2}'.format(
                            self.function_field_name,
                            action,
                            self.api_allowed_methods)
                        return Response(data=self.base_response,
                                        status=status.HTTP_403_FORBIDDEN)
                    _method = getattr(self, action)
                    output, debug, error = self._method_wrapper(data, _method, action)
                    self.base_response['debug'].update(debug)
                    self.base_response['data'] = output
                    if not error:
                        return Response(data=self.base_response, status=status.HTTP_200_OK)
                    else:
                        return Response(data=self.base_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except (AttributeError, ImportError) as error:
                    self.base_response['error'] = "{} not found".format(self.function_field_name)
                    self.base_response['debug'].update({"exception": str(error)})
                    return Response(data=self.base_response, status=status.HTTP_404_NOT_FOUND)
            self.base_response['error'] = "no {} in data".format(self.function_field_name)
            return Response(data=self.base_response, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, json.JSONDecodeError) as error:
            self.base_response["error"] = "general api error"
            if settings.DEBUG:
                self.base_response['debug'].update({'exception-type': str(type(error)), 'exception-args': error.args})
            return Response(data=self.base_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_base_response(self):
        if settings.DEBUG:
            return {'debug': {
                self.restifiy("api attributes"): {self.restifiy("api allowed methods"): self.api_allowed_methods}},
                'debug-mode': ["enabled", "to disable go to settings.py and change DEBUG=True to false"]}
        return {}

    def call_method(self, data, method):
        return method(data)

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

    def api_abstractions(self, data):
        """
        Implement this method in the complex api view
        change base response here according to new data
        :param data:
        :return:
        """
        return data
