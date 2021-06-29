import os
from django.db import models
from django.utils.text import Truncator
from django.contrib.sites.models import Site

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from .mixins import BaseModelMixin


User = get_user_model()


def upload_to(instance, filename):
    return f'files/{instance.user}/{filename}'


class FileQeryset(models.QuerySet):

    def site(self, site):
        return self.filter(site=site)

    def user(self, user):
        return self.filter(user=user)


class FileManager(models.Manager):

    def user(self, user):
        return self.get_queryset().active().user(user)

    def get_queryset(self, *args, **kwargs):
        return FileQeryset(self.model, *args, using=self._db, **kwargs)


class File(BaseModelMixin):
    # For filtering
    source_app = models.CharField(
        _("Source application"), max_length=150, 
        db_index=True, null=True, blank=True, editable=False)

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        related_name='files')
    # Uploader
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='files',
        blank=True, null=True
    )

    src = models.FileField(
        verbose_name=_("File"),
        help_text=_("Select a file"),
        upload_to=upload_to)

    objects = FileManager()

    class Meta:
        ordering = ('-created', '-updated',)
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return f'{self.src}'

    def save(self, *args, **kwargs):
        self.source_app = self._meta.app_label
        return super().save(*args, **kwargs)

    @property
    def name_truncated(self):
        return Truncator(self.name).chars(30)

    @property
    def name(self):
        return self.src.name.split('/')[-1]

    @property
    def filename(self):
        return self.src.name.split('/')[0]

    @property
    def ext(self):
        return os.path.splitext(self.name)[1]

    @property
    def size(self):
        return filesizeformat(self.src.size)
