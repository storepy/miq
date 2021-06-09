from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site as DjangoSite, SiteManager as DjangoSiteManager

from miq.models.mixins import BaseModelMixin


User = get_user_model()


class SiteManager(DjangoSiteManager):
    pass


class Site(BaseModelMixin, DjangoSite):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sites')

    objects = SiteManager()

    class Meta(DjangoSite.Meta):
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')
        ordering = ['domain']


class Navbar(BaseModelMixin):
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Navbar Settings')
        verbose_name_plural = _('Navbar Settings')

    def __str__(self):
        return f'{self.site} Navbar'

    site = models.OneToOneField(
        'miq.Site', on_delete=models.CASCADE,
        related_name='navbar',
    )
