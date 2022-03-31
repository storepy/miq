from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from miq.core.models.mixins import BaseModelMixin


User = get_user_model()


class Navbar(BaseModelMixin):
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Navbar Settings')
        verbose_name_plural = _('Navbar Settings')

    def __str__(self):
        return f'{self.site} Navbar'

    site = models.OneToOneField(
        'core.Site', on_delete=models.CASCADE,
        related_name='navbar',
    )
