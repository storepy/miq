
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import AuthenticationForm


"""
LOGIN VIEW
"""


class Mixin(object):

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LoginView(Mixin, auth_views.LoginView):
    """
    Available context variable: form, next, site, site_name
    https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.views.LoginView
    https://github.com/ubernostrum/django-registration
    """

    authentication_form = AuthenticationForm
    # template_name = 'miq/accounts/login.html'
