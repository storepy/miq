
from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from ..core.models import BaseModelMixin


def jsondef():
    return dict()


class Attempt(BaseModelMixin):
    site_id = models.CharField(max_length=200, default=settings.SITE_ID, null=True, blank=True)

    # session key
    username = models.CharField(max_length=500)

    # TODO: Use for core password validation
    password = models.CharField(max_length=500)

    payload = models.JSONField(_("Payload"), default=jsondef, blank=True, null=True)

    #
    url = models.TextField(max_length=500)
    path = models.TextField(max_length=500)
    referrer = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    ip = models.GenericIPAddressField(
        unpack_ipv4=True, verbose_name=_('Ip address'),
        null=True, blank=True)

    debug = models.BooleanField(default=settings.DEBUG)
    #

    def save(self, *args, **kwargs):
        self.referrer = self.referrer.lower()
        self.user_agent = self.user_agent.lower()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created', '-updated',)
        verbose_name = _('Login Attempt')
        verbose_name_plural = _('Login Attempts')

    def __str__(self):
        return f'{self.username}'


class AttemptDt(BaseModelMixin):
    attempt = models.ForeignKey("Attempt", verbose_name=_("Attempt"), on_delete=models.CASCADE, related_name='times')

    class Meta:
        ordering = ('-created', '-updated',)
        verbose_name = _('Login Attempt Datetime')
        verbose_name_plural = _('Login Attempt Datetimes')

    def __str__(self):
        return f'{self.created}'
