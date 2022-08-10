from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from .mixins import BaseModelMixin


def setting_config_dict() -> dict:
    return {
        'social_links': []
    }


class SiteSetting(BaseModelMixin):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE,
        related_name='settings', default=1)

    # CONTACT

    contact_number = models.CharField(
        max_length=20, blank=True, null=True,
        help_text=_('Preferred contact number'))
    contact_number_display = models.CharField(
        _("Contact number"), max_length=99,
        null=True, blank=True)
    contact_number_title = models.CharField(
        _("Contact number description"), max_length=99,
        null=True, blank=True)

    contact_email = models.EmailField(
        max_length=99, blank=True, null=True,
        help_text=_('Preferred contact email'))

    whatsapp_number = models.CharField(
        max_length=20, blank=True, null=True,
        help_text=_('International Whatsapp number'))
    whatsapp_link = models.URLField(
        _("Whatsapp link"), max_length=200,
        null=True, blank=True)
    whatsapp_link_title = models.CharField(
        _("Whatsapp link description"), max_length=99,
        null=True, blank=True)

    # LIVE STATUS

    is_live = models.BooleanField(
        default=False,
        help_text=_('Turn off to prevent access to your website'))

    # INFO

    ico = models.OneToOneField(
        "core.File", on_delete=models.SET_NULL, verbose_name=_("Favicon link"),
        related_name='ico', null=True, blank=True,
    )
    logo = models.OneToOneField(
        "core.Image", verbose_name=_("Logo"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='setting'
    )

    about = models.TextField(
        _("About us"), null=True, blank=True)
    about_html = models.TextField(
        _("About us html"), null=True, blank=True)

    faq = models.TextField(
        _("Frequently Asked Questions"), null=True, blank=True)
    faq_html = models.TextField(
        _("Frequently Asked Questions"), null=True, blank=True)

    terms = models.TextField(
        _("About us"), null=True, blank=True)
    terms_html = models.TextField(
        _("About us"), null=True, blank=True)

    privacy = models.TextField(
        _("About us"), null=True, blank=True)
    privacy_html = models.TextField(
        _("About us"), null=True, blank=True)

    # CLOSE TEMPLATE

    ct_title = models.CharField(max_length=200, blank=True, null=True)
    ct_text = models.TextField(blank=True, null=True)
    ct_html = models.TextField(blank=True, null=True)
    ct_image = models.OneToOneField(
        "core.Image", verbose_name=_("Close Image"),
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name='site_setting')

    # ANALYTICS

    ga_tracking = models.TextField(
        blank=True, null=True,
        verbose_name='Google Analytics Tracking ID',
        help_text='Google Analytics Measurement ID')

    fb_pixel = models.TextField(
        blank=True, null=True,
        verbose_name='Facebook Pixel ID',
        help_text='Facebook Pixel ID')

    fb_app_id = models.CharField(
        _("Facebook App ID"), max_length=500,
        blank=True, null=True,
    )
    fb_app_secret = models.CharField(
        _("Facebook App Secret"), max_length=500,
        blank=True, null=True,
    )

    #
    config = models.JSONField(default=setting_config_dict, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return f'Settings: {self.site}'

    def save(self, *args, **kwargs):
        self.config = {**setting_config_dict(), **self.config}
        super().save(*args, **kwargs)

    @property
    def display_contact_email(self):
        if self.contact_email:
            return self.contact_email.replace('@', '[at]')


# class AbstractLink(BaseModelMixin):
#     class Meta:
#         ordering = ('name', '-created')
#         abstract = True

#     name = models.CharField(_("Display name"), max_length=50)
#     url = models.URLField(_("Url"), max_length=250)
#     is_external = models.BooleanField(_("Open in new tab"), default=False)


# class SocialLink(AbstractLink):
#     def save(self, *args, **kwargs) -> None:
#         self.is_external = True
#         return super().save(*args, **kwargs)
