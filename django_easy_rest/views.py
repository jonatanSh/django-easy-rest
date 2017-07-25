from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .utils.search_model import GetModelByString
from .serializers import FullDebuggerSerializer
import json
from .mixins import MethodApiUnPackerMixin
from copy import copy


class MethodBasedApi(APIView):
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
                self.restifiy("api attributes"): {self.restifiy("api allowed methods"): self.api_allowed_methods}}}
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


class ModelMethodBasedApi(MethodApiUnPackerMixin, MethodBasedApi):
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
