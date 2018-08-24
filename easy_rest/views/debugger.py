import sys
import json
import traceback
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ..utils.utils import reverse_lazy
from uuid import uuid4
from rest_framework.response import Response
from django.http.response import HttpResponseForbidden, HttpResponseNotFound
from django.conf import settings
from base64 import b64encode, b64decode
from urllib.parse import unquote, quote


def decoder(data):
    data = unquote(data)
    if int(sys.version[0]) < 3:
        return json.loads(b64decode(data))
    return json.loads(b64decode(data).decode("utf-8"))


def encoder(data):
    if int(sys.version[0]) < 3:
        data = json.dumps(b64encode(data))
    else:
        data = b64encode(json.dumps(data).encode("utf-8"))
    return quote(data)


class DebugHandler(object):
    def __init__(self, request, data, status):
        self.request = request
        self.data = data
        self.status = status

    def handle(self):
        token = str(uuid4())
        debug_data = encoder({
            "token": token,
            "data": self.data
        })
        self.data['debug_url'] = reverse_lazy("easy_rest:debugger") + "?token={0}&debug_data={1}".format(token,
                                                                                                         debug_data)
        return Response(data=self.data, status=self.status)


class DebugObject(object):
    def __init__(self, tb, handler):
        self.tb = tb
        self.handler = handler
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

    def serialize(self):
        return {
            "error": repr(self.tb),
            "trace": self.get_trace(),
            "handler": self.handler,
        }

    def get_trace(self):
        return [t.lstrip().rstrip().replace("\n", "").replace("\r", "") for t in self.trace]


class DebugCache(object):
    def __init__(self):
        self.cache = []

    def update(self, tb, handler):
        self.cache.append(DebugObject(tb, handler).serialize())

    def serialize(self):
        data = []
        for obj in self.cache:
            data.append(obj)
        return data


class TbFile(object):
    data = ""

    def write(self, data):
        self.data += data

    def read(self):
        return self.data


def get_error(error):
    if hasattr(error, '__traceback__') and hasattr(error, 'tb_frame'):
        trace = ''.join(traceback.format_tb(error.__traceback__))
    else:
        trace = 'Unknown traceback object type({}) has no attribute __traceback__'.format(type(error))

    return trace


class DebugView(TemplateView):
    template_name = "easy_rest/debug.html"
    debug_data = {}

    def dispatch(self, request, *args, **kwargs):
        try:
            self.debug_data = decoder(request.GET.get("debug_data"))
        except:
            pass

        return super(DebugView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.debug_data:
            return HttpResponseNotFound("no debug data avilable")

        token = request.GET.get("token")

        if token != self.debug_data['token']:
            if settings.DEBUG:
                print("real token is ", self.debug_data['token'], "got", token)
            return HttpResponseForbidden("Invalid token")

        response = super(DebugView, self).get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        debug_data = self.debug_data['data']
        ctx = super(DebugView, self).get_context_data(**kwargs)
        if "input" in debug_data:
            request = debug_data["input"]
            request_data = request['request_data']
            ctx["api_input"] = json.dumps(request_data, indent=1)
            ctx["api_code"] = request["request_code"]
        if 'debug_url' in debug_data:
            del debug_data['debug_url']
        if "input" in debug_data:
            del debug_data['input']
        ctx['output'] = json.dumps(debug_data, indent=1)
        tb = self.request.session.get("last_debug_error")
        if tb:
            ctx['traceback'] = json.dumps(
                {"traceback": tb, "note": "the traceback is returned from the session and might be outdated"},
                indent=1)

        return ctx
