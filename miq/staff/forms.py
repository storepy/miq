from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from miq.auth.accounts.forms import AuthenticationForm


class StaffAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_staff:
            raise ValidationError(_('This account invalid'), code='invalid')
