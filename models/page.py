
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from miq.models.mixins import BaseModelMixin


__all__ = ['Index', 'Page', 'PageSectionMeta']


class AbstractPage(BaseModelMixin):
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=250, help_text=_('Page Meta title'),
        null=True, blank=True
    )

    def update_sections_source(self):
        to_update = self.sections.exclude(source=self.slug)
        if to_update.exists():
            to_update.update(source=self.slug)


# INDEX PAGE

class IndexManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related('sections').select_related('site')


class Index(AbstractPage):
    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = _('Index page')
        verbose_name_plural = _('Index page')

    # From abstract: title
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE,
        related_name='index')
    sections = models.ManyToManyField('miq.Section', blank=True)

    objects = IndexManager()


# PAGE


class PageQueryset(models.QuerySet):

    def parents(self):
        return self.filter(parent__isnull=True)

    def draft(self):
        return self.filter(is_published=False)

    def published(self):
        return self.filter(is_published=True)


class PageManager(models.Manager):

    def parents(self):
        return self.get_queryset().parents()

    def draft(self):
        return self.get_queryset().draft()

    def published(self):
        return self.get_queryset().published()

    def get_queryset(self, *args, **kwargs):
        return PageQueryset(self.model, *args, using=self._db, **kwargs)\
            .select_related('site')\
            .prefetch_related('sections')


class Page(AbstractPage):
    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = _('Page')
        verbose_name_plural = _('Page')

    def __str__(self):
        return f'{self.site.name} {self.label} page'

    def save(self, *args, **kwargs):

        if not self.slug_pk:
            self.slug_pk = uuid4()

        if self.is_published and not self.dt_published:
            self.dt_published = timezone.now()

        super().save(*args, **kwargs)

    # From Abstract:  title
    # From related: children

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        related_name='pages')

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        blank=True, null=True)

    # TODO: Idea: Linked list
    sections = models.ManyToManyField(
        'miq.Section', blank=True,
        through='PageSectionMeta',
        related_name='pages'
    )

    # MUST BE the same as related name
    source = models.CharField(max_length=100, blank=True, null=True)

    label = models.CharField(max_length=100, help_text=_('Page header label'))
    slug = models.SlugField(
        max_length=200, db_index=True, unique=True,
        default=uuid4
    )

    # For internal and system use
    slug_pk = models.SlugField(
        max_length=100, unique=True, db_index=True,
        editable=False, null=True,
    )

    is_published = models.BooleanField(
        default=False, help_text=_('Publish this page'))
    dt_published = models.DateTimeField(
        blank=True, null=True, help_text=_('Publication date'))

    objects = PageManager()

    @property
    def updated_since(self):
        return timesince(self.updated)

    @property
    def detail_url(self):
        if not self.is_published:
            return

        if self.source:
            obj = getattr(self, f'{self.source}')
            if obj:
                try:
                    return obj.detail_url
                except Exception:
                    pass

        return

    def has_children(self):
        return self.children.exists()

    def publish(self):
        self.is_published = True
        self.save()


# PAGE SECTION META


class PageSectionMeta(BaseModelMixin):
    class Meta:
        ordering = ('-created', '-updated')
        # Do not add same sections to multiple pages
        constraints = [
            models.UniqueConstraint(
                fields=['page', 'section'], name='unique_page_section')
        ]

    page = models.ForeignKey('miq.Page', on_delete=models.CASCADE)
    section = models.ForeignKey(
        'miq.Section', on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.section and self.page and self.section.source != self.page.slug:
            self.section.source = self.page.slug
            self.section.save()

    def __str__(self):
        return f'{self.page}, section[{self.section}] {self.section.position}'
