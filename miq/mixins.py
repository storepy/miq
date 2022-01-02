from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Template
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin


class ModelSerializerMixin:
    def get_request(self):
        try:
            return self._kwargs.get('context').get('request')
        except Exception:
            return None


class RendererMixin:
    def _render(self, template_name: str, context: dict = {}):

        if '.html' in template_name:
            return render_to_string(template_name, context)

        return Template(str(template_name)).render(Context(context))


class DevLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'OPTIONS' and settings.DEBUG is True:
            return HttpResponse()

        return super().dispatch(request, *args, **kwargs)


class StaffLoginRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'OPTIONS' and settings.DEBUG is True:
            return HttpResponse()

        if not request.user.is_staff:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
