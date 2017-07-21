from functools import wraps


def api_method(func, help_message=None):
    if help_message is None:
        help_message = {"general": "Help for this rest not implemented"}

    @wraps(func)
    def wrapper(*args, **kwargs):
        return _ApiMethod(method=func, help_message=help_message)

    return wrapper


class _ApiMethod(object):
    def __init__(self, method, help_message):
        self.method = method
        if type(help_message) is not dict:
            self.help_message = {"general": help_message}
        else:
            self.help_message = help_message
        if 'general' not in help_message:
            help_message["general"] = "Help for this rest not implemented"

    def get_help(self, prefix='general'):
        if prefix in self.help_message:
            return {"help": self.help_message[prefix]}
        else:
            return {"help": self.help_message['general'], "help-list": "help list {}".format(self.help_message.keys())}

    def __call__(self, data):
        return self.method(data)
