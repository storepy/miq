import datetime
from uuid import uuid4
from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseDateQsMixin:
    def updated_today(self):
        today = date.today()
        return self.filter(
            updated__day=today.day, updated__year=today.year,
            updated__month=today.month).order_by('-updated')

    def updated_yesterday(self):
        yst = date.today() - datetime.timedelta(1)
        return self.filter(
            updated__day=yst.day, updated__year=yst.year,
            updated__month=yst.month).order_by('-updated')

    def created_today(self):
        today = date.today()
        return self.filter(
            created__day=today.day, created__year=today.year,
            created__month=today.month).order_by('-created')

    def created_yesterday(self):
        yst = date.today() - datetime.timedelta(1)
        return self.filter(
            created__day=yst.day, created__year=yst.year,
            created__month=yst.month).order_by('-created')

    def get_last_n_days(self, days_count: int):
        day = date.today() - datetime.timedelta(days=days_count)
        return self.filter(created__gte=day).order_by('-created')
        # return self.filter(
        #     created__day__gte=day.day, created__year__gte=day.year,
        #     created__month__gte=day.month).order_by('-created')


class BaseManagerMixin(BaseDateQsMixin):
    pass


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
    Abstract Model Class whic adds the following fields to a model:
    - slug_public
    - meta_title
    - meta_description
    - label
    - is_published
    - dt_published
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
