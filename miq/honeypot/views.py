import logging
import datetime

from django.http import HttpResponseBadRequest
from django.utils import timezone
# from django.utils.translation import gettext_lazy as _

from ..core.views.generic import CreateView
from ..core.utils import get_ip, request_body_to_dict, get_request_url

from .models import Attempt, AttemptDt

logger = logging.getLogger(__name__)


def log_attempt(request, /, **kwargs):
    # log a login attempt

    filter = {
        'username': request.POST.get('username'),
        'password': request.POST.get('password'),
        'ip': get_ip(request),
        'url': get_request_url(request),
        'path': request.path,
        'site_id': request.site.id,
    }

    last = Attempt.objects.filter(**filter)
    attempt = None

    if last.exists() and (_ := last.order_by('-created').first()):
        attempt = _
        # _.save()
    else:
        attempt = Attempt.objects.create(**{
            **filter,
            'payload': request.POST or request_body_to_dict(request),
            'referrer': request.META.get('HTTP_REFERER'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        })

    if attempt:
        if not AttemptDt.objects.filter(attempt=attempt, created__gt=timezone.now() - datetime.timedelta(minutes=1)).exists():
            AttemptDt.objects.create(attempt=attempt)

        logger.warning(f'Login attempt: {attempt.slug}')


class LoginAttemptView(CreateView):
    model = Attempt
    fields = ['username', 'password']
    template_name = 'honeypot/login.django.html'
    # success_url = reverse_lazy('honeypot:login')

    def form_valid(self, form):
        log_attempt(self.request)
        return self.render_to_response(self.get_context_data(form=form), status=HttpResponseBadRequest.status_code)

    def form_invalid(self, form):
        log_attempt(self.request)
        return self.render_to_response(self.get_context_data(form=form), status=HttpResponseBadRequest.status_code)
