
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _


from .mixins import BaseModelMixin


__all__ = ['Index', 'Page',
           # 'PageSectionMeta'
           ]


class AbstractPage(BaseModelMixin):
    """
    Adds the following fields:
    - title : CharField, max_length 250, null, blank
    """
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=250, help_text=_('Page Meta title'),
        null=True, blank=True
    )
    # meta_title
    # meta_description
    # meta_keywords

    def update_sections_source(self):
        to_update = self.sections.exclude(source=self.slug)
        if to_update.exists():
            to_update.update(source=self.slug)


"""
# INDEX PAGE
"""


class IndexManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
            .prefetch_related('sections')\
            .select_related('site')


class Index(AbstractPage):
    """
    Has the following fields:
    - site: OneToOneField, cascades on delete
    - title : CharField, max_length 250, null, blank
    - sections: ManyToManyField, blank
    """
    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = _('Index page')
        verbose_name_plural = _('Index page')

    # From abstract: title
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE,
        related_name='index')
    cover = models.OneToOneField(
        'core.Image', verbose_name=_("Cover"), on_delete=models.SET_NULL,
        blank=True, null=True
    )
    sections = models.ManyToManyField(
        'core.Section', blank=True, related_name='index')

    objects = IndexManager()


"""
# PAGE
"""


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
            .select_related('site')
        # .prefetch_related('sections')


class Page(AbstractPage):
    """
    Has the following fields:
    - site: OneToOneField, CASCADE, related_name: pages
    - title: CharField, max_length 250, null, blank
    - label: CharField, max_length 100
    - source: CharField, max_length 100, null, blank
    - meta_slug: SlugField, max_length 100, db_index, unique, default: uuid4
    - parent: ForeignKey, CASCADE, related_name: children
    - sections: ManyToManyField, blank, related_name: pages
    - is_published: BooleanField, False
    - dt_published: DateTimeField, blank, null
    """
    # From Abstract:  title
    # From related: children

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        related_name='pages')

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        blank=True, null=True)

    # TODO: Idea: Linked list
    # sections = models.ManyToManyField(
    #     'core.Section', blank=True,
    #     through='PageSectionMeta',
    #     related_name='pages'
    # )

    # MUST BE the same as related name
    source = models.CharField(max_length=100, blank=True, null=True)

    label = models.CharField(max_length=100, help_text=_('Page header label'))

    # For public display
    meta_slug = models.SlugField(
        max_length=100, unique=True, db_index=True,
        default=uuid4
    )

    is_published = models.BooleanField(
        default=False, help_text=_('Publish this page'))
    dt_published = models.DateTimeField(
        blank=True, null=True, help_text=_('Publication date'))

    objects = PageManager()

    def save(self, *args, **kwargs):
        if self.meta_slug:
            self.meta_slug = slugify(self.meta_slug)

        if self.is_published and not self.dt_published:
            self.dt_published = timezone.now()

        super().save(*args, **kwargs)

        # sections = self.sections.exclude(source=self.slug)
        # if sections.exists():
        #     sections.update(source=self.slug)

    def __str__(self):
        return f'{self.label}[{self.site.name}]'

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = _('Page')
        verbose_name_plural = _('Page')

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


"""
# PAGE SECTION META
"""


# class PageSectionMeta(BaseModelMixin):
#     class Meta:
#         ordering = ('-created', '-updated')
#         # Do not add same sections to multiple pages
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['page', 'section'], name='unique_page_section')
#         ]

#     page = models.ForeignKey('core.Page', on_delete=models.CASCADE)
#     section = models.ForeignKey(
#         'core.Section', on_delete=models.CASCADE,
#     )

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         if self.section and self.page\
#                 and self.section.source != self.page.slug:
#             self.section.source = self.page.slug
#             self.section.save()

#     def __str__(self):
#         return f'{self.page}, section[{self.section}] {self.section.position}'
