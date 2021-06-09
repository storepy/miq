from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class DevLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'OPTIONS' and settings.DEBUG is True:
            return HttpResponse()

        return super().dispatch(request, *args, **kwargs)
