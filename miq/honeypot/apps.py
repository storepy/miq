from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MiqStaffConfig(AppConfig):
    name = 'miq.honeypot'
    verbose_name = _('Honeypot')
    verbose_name_plural = _('Honeypot')
    default_auto_field = 'django.db.models.BigAutoField'
