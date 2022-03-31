from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin as DjLoginRequiredMixin


class LoginRequiredMixin(DjLoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'OPTIONS' and settings.DEBUG is True:
            return HttpResponse()

        if not request.user.is_staff:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
