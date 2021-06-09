from django.db import models
from django.contrib.sites.models import Site

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .mixins import BaseModelMixin


User = get_user_model()


def upload_to(instance, filename):
    return f'images/{instance.user}/{filename}'


class ImageQeryset(models.QuerySet):

    def site(self, site):
        return self.filter(site=site)

    def user(self, user):
        return self.filter(user=user)

    def active(self):
        return self.filter(is_active=True)


class ImageManager(models.Manager):

    def user(self, user):
        return self.get_queryset().active().user(user)

    def active(self):
        return self.get_queryset().active()

    def get_queryset(self, *args, **kwargs):
        return ImageQeryset(self.model, *args, using=self._db, **kwargs)


class Image(BaseModelMixin):

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        related_name='images')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='images')

    src = models.ImageField(
        verbose_name="Source",
        help_text="Select an image file",
        upload_to=upload_to)

    caption = models.CharField(max_length=400, blank=True)
    alt_text = models.CharField(max_length=400, blank=True)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1)

    objects = ImageManager()

    class Meta:
        ordering = ('-updated', '-created',)
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'{self.src.name}'
