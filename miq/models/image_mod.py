from django.db import models
from django.contrib.sites.models import Site

from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.template import Context, Template
from django.template.loader import render_to_string

from .mixins import BaseModelMixin

from miq.utils_img import get_thumbnail, crop_img_to_square


User = get_user_model()


def upload_to(instance, filename):
    return f'images/{instance.user}/{filename}'


def upload_thumb_to(instance, filename):
    return f'images/thumbs/{filename}'


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


class RendererMixin:
    def render_thumb_sq(self):
        return self._render(
            'miq/components/img-square.html',
            context={'img': self, **self.to_json()}
        )

    def render(self):
        return self._render(
            'miq/components/img.html',
            context={'img': self, **self.to_json()}
        )

    def _render(self, template_name: str, context: dict = {}):

        if '.html' in template_name:
            return render_to_string(template_name, context)

        return Template(str(template_name)).render(Context(context))


class Image(RendererMixin, BaseModelMixin):

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        related_name='images')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='images')

    src = models.ImageField(
        max_length=500,
        verbose_name="Source",
        help_text="Select an image file",
        upload_to=upload_to)
    thumb_sq = models.ImageField(
        max_length=500,
        verbose_name="Square Thumbnail",
        help_text="Select an image file",
        upload_to=upload_thumb_to,
        null=True, blank=True)
    thumb = models.ImageField(
        max_length=500,
        verbose_name="Thumbnail",
        help_text="Select an image file",
        upload_to=upload_thumb_to,
        null=True, blank=True)
    # thumbnails = models.ManyToManyField(
    #     "miq.Thumbnail", verbose_name=_("Thumbnails"), blank=True)

    caption = models.CharField(max_length=400, blank=True)
    alt_text = models.CharField(max_length=400, blank=True)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1)

    objects = ImageManager()

    class Meta:
        ordering = ('-updated', '-created', 'position')
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'{self.src}'

    def save(self, *args, **kwargs):
        self.thumb.save(
            self.src.url.split('/')[-1],
            self.src.file, save=False)
        self.thumb_sq.save(
            self.src.url.split('/')[-1],
            self.src.file, save=False)

        super().save(*args, **kwargs)

        try:
            get_thumbnail(file=self.thumb).save(self.thumb.path)
            crop_img_to_square(file=self.thumb).save(self.thumb_sq.path)
        except Exception:
            pass

    @property
    def name_truncated(self):
        return Truncator(self.name).chars(30)

    @property
    def name(self):
        return f'{self.src.name}'

    @property
    def width(self):
        return self.src.width

    @property
    def height(self):
        return self.src.height

    @property
    def size(self):
        return filesizeformat(self.src.size)

    def to_json(self):
        """Serialize an image"""

        data = {
            'src': f'{self.src.url}',
            'width': self.width,
            'height': self.height,
            'alt_text': self.alt_text or '',
        }

        if self.thumb:
            data['thumb'] = f'{self.thumb.url}'
            data['thumb_width'] = self.thumb.width
            data['thumb_height'] = self.thumb.height

        if self.thumb_sq:
            data['thumb_sq'] = f'{self.thumb_sq.url}'
            data['thumb_sq_width'] = self.thumb_sq.width
            data['thumb_sq_height'] = self.thumb_sq.height

        return data

    def deactivate(self):
        self.is_active = False
        self.save()


# Thumbnail
# Sizes


class Thumbnail(RendererMixin, BaseModelMixin):
    class Meta:
        ordering = ('-updated', '-created')
        verbose_name = _('Thumbnail')
        verbose_name_plural = _('Thumbnails')

    def __str__(self):
        return f'{self.src}'

    image = models.ForeignKey(
        "miq.Image",
        verbose_name=_("Original Image"),
        on_delete=models.CASCADE,
        related_name='thumbnails'
    )

    src = models.ImageField(
        max_length=500,
        verbose_name="Thumbnail",
        help_text="Select an image file",
        upload_to=upload_thumb_to,
        null=True, blank=True
    )
    is_square = models.BooleanField(default=False)
