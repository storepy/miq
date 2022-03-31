from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MiqStaffConfig(AppConfig):
    name = 'miq.staff'
    verbose_name = _('Staff Management')
    verbose_name_plural = _('Staff Management')
    default_auto_field = 'django.db.models.BigAutoField'
