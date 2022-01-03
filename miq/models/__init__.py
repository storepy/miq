from django.db import models
# from django.utils.text import Truncator
from django.contrib.sites.models import Site
# from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from miq.utils import get_text_choices

from .user_mod import User, UserGender
from .image_mod import Image, Thumbnail
from .file_mod import File
from .page_mod import Index, Page, PageSectionMeta
from .section_mod import *

from .mixins import BaseModelMixin


UserGenders = get_text_choices(UserGender)


__all__ = (
    'BaseModelMixin',
    'User', 'UserGender', 'UserGenders',
    'Image', 'Thumbnail', 'File',
    'Index', 'Page', 'PageSectionMeta',

    'SiteSetting', 'SocialLink',
    # 'SectionType', 'Section', 'SectionImageMeta',
    # 'ImageSection', 'MarkdownSection', 'TextSection', 'JumbotronSection
)


class SiteSetting(BaseModelMixin):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE,
        related_name='settings', default=1)

    # CONTACT
    contact_number = models.CharField(
        max_length=20, blank=True, null=True,
        help_text=_('Preferred contact number'))
    contact_email = models.EmailField(
        max_length=99, blank=True, null=True,
        help_text=_('Preferred contact email'))
    #

    is_live = models.BooleanField(
        default=False,
        help_text=_('Turn off to prevent access to your website'))

    # LOGO

    logo = models.OneToOneField(
        "miq.Image", verbose_name=_("Logo"),
        on_delete=models.SET_NULL, null=True, blank=True
    )

    # ANALYTICS

    ga_tracking = models.TextField(
        blank=True, null=True,
        verbose_name='Google Analytics Tracking ID',
        help_text='Google Analytics Measurement ID')

    fb_pixel = models.TextField(
        blank=True, null=True,
        verbose_name='Facebook Pixel ID',
        help_text='Facebook Pixel ID')

    # CLOSE TEMPLATE

    ct_title = models.CharField(max_length=200, blank=True, null=True)
    ct_text = models.TextField(blank=True, null=True)
    ct_html = models.TextField(blank=True, null=True)
    ct_image = models.OneToOneField(
        "miq.Image", verbose_name=_("Close Image"),
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name='site_setting')

    # SOCIAL LINKS

    links = models.ManyToManyField(
        'miq.SocialLink', verbose_name=_("Social links"), blank=True,)

    #
    # extra = models.JSONField(default=setting_extra, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return f'Settings: {self.site}'

    # def save(self, *args, **kwargs):
    #     self.extra = {**setting_extra(), **self.extra}
    #     super().save(*args, **kwargs)

    @property
    def display_contact_email(self):
        if self.contact_email:
            return self.contact_email.replace('@', '[at]')


"""
# LINK
"""


class AbstractLink(BaseModelMixin):
    class Meta:
        ordering = ('name', '-created')
        abstract = True

    name = models.CharField(_("Display name"), max_length=50)
    url = models.URLField(_("Url"), max_length=250)
    is_external = models.BooleanField(_("Open in new tab"), default=False)


class SocialLink(AbstractLink):
    def save(self, *args, **kwargs) -> None:
        self.is_external = True
        return super().save(*args, **kwargs)
