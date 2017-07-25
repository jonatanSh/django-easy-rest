from django.conf import settings


class MethodApiUnPackerMixin(object):
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


class MethodApiHelpMixin(object):
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


class DecorativeKeysMethodApi(object):
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
