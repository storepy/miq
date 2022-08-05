
from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from ...core.models import BaseModelMixin

from .managers import HitManager, HitPublicManager


def jsondef():
    return dict()


class Landing(BaseModelMixin):
    name = models.SlugField(_("Name"), max_length=99, unique=True, db_index=True)
    is_pinned = models.BooleanField(_("Is pinned"), default=False)
    # hits = models.ManyToManyField("analytics.Hit", verbose_name=_("Hits"), blank=True)

    def hits(self):
        key = f'p/{self.name}'
        return Hit.objects.filter(
            models.Q(path__icontains=key) | models.Q(referrer__icontains=key)
        ).distinct()

    class Meta:
        verbose_name = _('Landing')
        verbose_name_plural = _('Landing')
        ordering = ('-is_pinned', '-updated', '-created')


class Hit(BaseModelMixin):

    site_id = models.CharField(max_length=500)

    # unique identidier, could be a slug for customer, uid for user, etc
    source_id = models.CharField(max_length=500, blank=True, null=True)

    # session key
    app = models.CharField(max_length=300, null=True, blank=True)
    model = models.CharField(max_length=300, null=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.referrer:
                self.referrer = self.referrer.lower()

            if self.user_agent:
                self.user_agent = self.user_agent.lower()

        return super().save(*args, **kwargs)

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


class Campaign(BaseModelMixin):
    key = models.CharField(max_length=99)
    value = models.CharField(_("Term"), max_length=99)
    ip = models.GenericIPAddressField(
        unpack_ipv4=True, verbose_name=_('Ip address'),
        null=True, blank=True)

    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
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
