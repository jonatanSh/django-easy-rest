from .. import views
from ..mixins import DecorativeKeysMethodApi, MethodApiHelpMixin


class MethodBased(DecorativeKeysMethodApi, MethodApiHelpMixin, views.ModelMethodBasedApi):
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

    def get_username(self, user):
        return {"username": user.username}

    def test(self, data):
        return {"new action": "test"}
