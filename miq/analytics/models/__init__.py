
from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from ...core.models import BaseModelMixin

from .managers import HitManager, HitPublicManager


def jsondef():
    return dict()


class Hit(BaseModelMixin):

    site_id = models.CharField(max_length=500)

    # unique identidier, could be a slug for customer, uid for user, etc
    source_id = models.CharField(max_length=500, blank=True, null=True)

    # session key
    session = models.CharField(max_length=300)
    session_data = models.JSONField(_("Session Data"), default=jsondef)
    url = models.TextField(max_length=500)
    path = models.TextField(max_length=500)
    referrer = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    ip = models.GenericIPAddressField(
        unpack_ipv4=True, verbose_name=_('Ip address'),
        null=True, blank=True)

    method = models.CharField(
        _("Request method"), max_length=50, null=True, blank=True)
    response_status = models.PositiveIntegerField(blank=True, null=True)
    debug = models.BooleanField(default=settings.DEBUG)

    #

    objects = HitManager()
    public = HitPublicManager()

    class Meta:
        ordering = ('-created', '-updated',)
        verbose_name = _('Hit')
        verbose_name_plural = _('Hits')

    def __str__(self):
        return f'{self.response_status}: {self.path}'


class SearchTerm(BaseModelMixin):
    session = models.CharField(max_length=300)
    value = models.CharField(_("Term"), max_length=99)
    count = models.PositiveIntegerField(_("Count"), default=1)

    class Meta:
        verbose_name = _('Search Term')
        verbose_name_plural = _('Search Terms')
        ordering = ('-updated', '-created',)


# class HitRangeUnit(models.TextChoices):
#     HOUR = 'HOUR', _('Hour')
#     DAY = 'DAY', _('Day')
#     WEEK = 'DAY', _('Day')
#     MONTH = 'DAY', _('Day')
#     YEAR = 'YEAR', _('Year')


# class HitRange:
#     unit = models.CharField(
# _("Type"), choices=HitRangeUnit.choices max_length=10)
#     unit_count = models.PositiveIntegerField(_("Unit count"), default=1)
#     start_dt = models.DateTimeField(_("Starts at"),)
#     end_dt = models.DateTimeField(_("Ends at"),)
#     hits = models.ManyToManyField(
# "Hit", verbose_name=_("Hits"), reverse_name="ranges")


# class IpAddress(models.Model):
#     class Meta:
#         ordering = ('value', )
#         verbose_name = _('IP Address')
#         verbose_name_plural = _('IP Addresses')

#     def __str__(self):
#         return f'{self.value}'

#     value = models.GenericIPAddressField(
#         unpack_ipv4=True, null=True,
#         verbose_name=_('Ip address'), blank=True)
#     is_blacklisted = models.BooleanField(default=False)
