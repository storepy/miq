
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ...core.models import BaseModelMixin

from .managers import HitManager, ViewsManager, BotsManager, ErrorsManager, LIBManager


def jsondef():
    return dict()


User = get_user_model()

# ========================== Link in Bio ==========================


class LIB(BaseModelMixin):
    name = models.SlugField(_("Name"), max_length=99, unique=True, db_index=True)
    utm_medium = models.TextField(blank=True, null=True, help_text="social")
    utm_source = models.TextField(blank=True, null=True, help_text="instabio")
    utm_content = models.TextField(blank=True, null=True, help_text="")

    is_pinned = models.BooleanField(_("Is pinned"), default=False)

    #
    hits = models.ManyToManyField("Hit", verbose_name=_("Hits"), blank=True)
    #

    objects = LIBManager()

    class Meta:
        verbose_name = _('Link in bio')
        verbose_name_plural = _('Links in bio')
        ordering = ('-is_pinned', '-updated', '-created')

    def __str__(self) -> str:
        return f'{self.name}'

#
# ========================== HITS ==========================
#


# class Device(BaseModelMixin):
#     name = models.CharField(_("Name"), max_length=99, null=True, blank=True)
#     user_agent = models.TextField(unique=True, db_index=True)
#     is_mobile = models.BooleanField(_("Is mobile"), default=False)

#     class Meta:
#         verbose_name = _('Device')
#         verbose_name_plural = _('Devices')
#         ordering = ('-updated', '-created')

#     def __str__(self) -> str:
#         return f'{self.user_agent}'


class AbstractVisitor(BaseModelMixin):

    user_agent = models.TextField(blank=True, null=True)
    ip = models.GenericIPAddressField(
        unpack_ipv4=True, verbose_name=_('Ip address'),
        null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-created', '-updated',)


class Visitor(AbstractVisitor):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='visitors', blank=True, null=True)

    is_bot = models.BooleanField(_('Is bot'), default=False)

    is_parsed = models.BooleanField(_("Is parsed"), default=False)

    city = models.CharField(_("City"), max_length=99, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=99, blank=True, null=True)
    countryCode = models.CharField(_("Country Code"), max_length=99, blank=True, null=True)
    region = models.CharField(_("Region"), max_length=99, blank=True, null=True)
    regionName = models.CharField(_("Region Name"), max_length=99, blank=True, null=True)
    zip = models.FloatField(_("Zip"), blank=True, null=True)

    currency = models.CharField(_("Currency"), max_length=99, blank=True, null=True)
    timezone = models.CharField(_("Timezone"), max_length=99, blank=True, null=True)

    mobile = models.BooleanField(_("Is parsed"), default=False)
    proxy = models.BooleanField(_("Is parsed"), default=False)

    asfullname = models.CharField(_("As"), max_length=99, blank=True, null=True)
    asname = models.CharField(_("As Name"), max_length=99, blank=True, null=True)
    org = models.CharField(_("Org"), max_length=99, blank=True, null=True)
    isp = models.CharField(_("ISP"), max_length=99, blank=True, null=True)

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
        ordering = ('-updated', '-created')

    def __str__(self) -> str:
        return f'{self.ip}'


class Hit(AbstractVisitor):
    site_id = models.CharField(max_length=500)

    visitor = models.ForeignKey("Visitor", verbose_name=_("Visitor"), on_delete=models.SET_NULL, null=True, blank=True)

    # unique identidier, could be a slug for customer, uid for user, etc
    source_id = models.CharField(max_length=500, blank=True, null=True)
    app = models.CharField(max_length=300, null=True, blank=True)
    model = models.CharField(max_length=300, null=True, blank=True)

    # session key
    session = models.CharField(max_length=300)
    session_data = models.JSONField(_("Session Data"), default=jsondef)

    #
    url = models.TextField(max_length=500)
    path = models.TextField(max_length=500)
    referrer = models.TextField(blank=True, null=True)

    # # visitor
    # user_agent = models.TextField(blank=True, null=True)
    # ip = models.GenericIPAddressField(
    #     unpack_ipv4=True, verbose_name=_('Ip address'),
    #     null=True, blank=True)

    #
    method = models.CharField(
        _("Request method"), max_length=50, null=True, blank=True)
    response_status = models.PositiveIntegerField(blank=True, null=True)
    debug = models.BooleanField(default=settings.DEBUG)

    #
    is_bot = models.BooleanField(_('Is bot'), default=False)
    is_parsed = models.BooleanField(_('Is parsed'), default=False)
    parsed_data = models.JSONField(_("Parsed Data"), default=jsondef)

    #

    objects = HitManager()
    views = ViewsManager()
    bots = BotsManager()
    errors = ErrorsManager()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.pk:
            if self.referrer:
                self.referrer = self.referrer.lower()

            if self.user_agent:
                self.user_agent = self.user_agent.lower()

        super().save(*args, **kwargs)

        if is_new and self.is_bot:
            try:
                Bot.objects.get_or_create(ip=self.ip, user_agent=self.user_agent)
            except Exception:
                pass

    class Meta:
        ordering = ('-created', '-updated',)
        verbose_name = _('Hit')
        verbose_name_plural = _('Hits')

    def __str__(self):
        return f'{self.response_status}: {self.path}'


class Bot(AbstractVisitor):
    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bot')
        ordering = ('-created', '-updated')

    def __str__(self) -> str:
        return f'{self.ip}'
