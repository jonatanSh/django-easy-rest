class MethodUnPackerMixin(object):
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
