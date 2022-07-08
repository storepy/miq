from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MiqAnalyticsConfig(AppConfig):
    name = 'miq.analytics'
    verbose_name = _('Analytics')
    verbose_name_plural = _('Analytics')
    default_auto_field = 'django.db.models.BigAutoField'

    # def ready(self):
    #     from . import signals
