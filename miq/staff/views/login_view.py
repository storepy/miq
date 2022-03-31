from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _


class AuthenticationForm(auth_forms.AuthenticationForm):
    def clean_username(self):
        return self.cleaned_data.get('username').lower()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_staff:
            raise ValidationError(_('This account invalid'), code='invalid')


class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    template_name = 'staff/login.django.html'

    def get_redirect_url(self):
        return reverse_lazy('staff:index')
