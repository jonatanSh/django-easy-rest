from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ..utils.utils import reverse_lazy
from uuid import uuid4
from rest_framework.response import Response
from django.http.response import HttpResponseForbidden


class DebugHandler(object):
    def __init__(self, request, data, status):
        self.request = request
        self.data = data
        self.status = status

    def handle(self):
        token = str(uuid4())
        self.request.session['debug_info_api'] = {
            "token": token,
            "data": self.data
        }
        self.data['debug']['url'] = reverse_lazy("easy_rest:debugger") + "?token={}".format(token)
        return Response(data=self.data, status=self.status)


class DebugView(TemplateView):
    template_name = "easy_rest/debug.html"

    def get(self, request, *args, **kwargs):
        debug_data = self.request.session.get("debug_info_api")
        if not debug_data:
            return HttpResponseForbidden()
        token = request.GET.get("token")

        if token != debug_data['token']:
            return HttpResponseForbidden("Invalid token")

        response = super(DebugView, self).get(request, *args, **kwargs)

        return response
