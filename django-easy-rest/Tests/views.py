from .. import views


class MethodBased(views.MethodApiView):
    method_helpers = {'special_error': {"help": {"general": "this is a special message"}},
                      'super_special': {"help": {"general": "general help",
                                                 "another": "another help"}}}
    api_allowed_methods = ['__all__']

    def correct(self, data):
        return {"test": "test"}

    def error(self, data):
        return 1 / 0

    def special_error(self, data):
        return 1 / 0

    def super_special(self, data):
        return 1 / 0

    def two_parms(self, a, b):
        return {"a---": a, "-b-": b}
