from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModelMixin(models.Model):
    """
    Abstract Model class with creation and modification datetimes
    ['site', 'created', 'updated']
    """

    slug = models.SlugField(
        max_length=100, unique=True, db_index=True,
        default=uuid4, editable=False
    )

    created = models.DateTimeField(
        ("creation date and time"),
        editable=False,
        auto_now_add=True,)

    updated = models.DateTimeField(
        ("update date and time"),
        auto_now=True,
        editable=False
    )

    def get_hit_data(self):
        return {
            'app': self._meta.app_label.lower(),
            'model': self._meta.model_name.lower(),
        }

    class Meta:
        abstract = True


class PublicBaseModelMixin(BaseModelMixin):
    """
    Abstract Model Class
    Adds meta_title, meta_description fields to a model
    """

    # SEO
    meta_title = models.CharField(
        max_length=250, help_text=_('Meta title'),
        null=True, blank=True
    )
    meta_desc = models.TextField(_("Meta description"), null=True, blank=True)
    # For public display an
    slug_public = models.SlugField(
        max_length=100, unique=True, db_index=True,
        default=uuid4
    )

    # Page
    label = models.CharField(max_length=100, help_text=_('Header label'))

    # conf
    is_published = models.BooleanField(
        default=False, help_text=_('Publish this object'))
    dt_published = models.DateTimeField(
        blank=True, null=True, help_text=_('Publication date'))

    class Meta:
        abstract = True
