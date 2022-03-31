from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MiqAuthConfig(AppConfig):
    name = 'miqauth'
    verbose_name = _('Members')
    verbose_name_plural = _('Members')
    default_auto_field = 'django.db.models.BigAutoField'
