import os

from django.db.models.functions import Concat
from django.db.models import CharField, Value
from django.db import models
from django.contrib.sites.models import Site

from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from ..mixins import RendererMixin
from ..middleware import local
from ..utils import get_image_files_path, img_file_from_pil, get_file_ext
from ..utils_img import get_thumbnail, crop_img_to_square

from .mixins import BaseModelMixin


User = get_user_model()


def upload_to(instance, filename):
    return f'images/{filename}'


def upload_thumb_to(instance, filename):
    return f'images/thumbs/{filename}'


class ImageQeryset(models.QuerySet):

    def site(self, site):
        return self.filter(site=site)

    def user(self, user):
        return self.filter(user=user)

    def active(self):
        return self.filter(is_active=True)

    def delete(self, *args, **kwargs):
        paths = []
        if self.exists():
            for img in self:
                paths.extend(get_image_files_path(img))

        r = super().delete(*args, **kwargs)

        if paths:
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
        return r


class ImageManager(models.Manager):

    def update_alt_texts(self, value: str, *, with_position=True):
        if not isinstance(value, str):
            return self

        if not with_position:
            return self.update(alt_text=value)

        alt_text = Concat(Value(f'{value} '), 'position', output_field=CharField())
        return super().update(alt_text=alt_text)

    def user(self, user):
        return self.get_queryset().active().user(user)

    def active(self):
        return self.get_queryset().active()

    def get_queryset(self, *args, **kwargs):
        return ImageQeryset(self.model, *args, using=self._db, **kwargs)


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
    src_mobile = models.ImageField(
        max_length=500,
        verbose_name="Source mobile",
        help_text="Select an image file",
        upload_to=upload_thumb_to,
        null=True, blank=True)

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

    caption = models.CharField(max_length=400, blank=True)
    alt_text = models.CharField(max_length=400, blank=True)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1)

    objects = ImageManager()

    class Meta:
        ordering = ('position', '-updated', '-created')
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'{self.src}'

    def save(self, *args, **kwargs):

        if not hasattr(self, 'site') and local and local.site:
            self.site = local.site

        if not hasattr(self, 'user') and local and local.user:
            user = local.user
            if user.is_authenticated:
                self.user = user

        if not self.pk:
            filename = self.src.url.split('/')[-1]  # type: str
            ext = get_file_ext(self.src.path)  # type: str
            if isinstance(ext, str) and ext.startswith('.'):
                ext = ext[1:]

            thumb = img_file_from_pil(get_thumbnail(file=self.src))
            self.src_mobile.save(filename, thumb, save=False)
            self.thumb.save(filename, thumb, save=False)

            crop = crop_img_to_square(file=self.thumb)
            self.thumb_sq.save(filename, img_file_from_pil(crop), save=False)

        super().save(*args, **kwargs)

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

    @property
    def width_mobile(self):
        if self.src_mobile:
            return self.src_mobile.width

    @property
    def height_mobile(self):
        if self.src_mobile:
            return self.src_mobile.height

    @property
    def size_mobile(self):
        if self.src_mobile:
            return filesizeformat(self.src_mobile.size)

    @property
    def width_thumb(self):
        if self.thumb:
            return self.thumb.width

    @property
    def height_thumb(self):
        if self.thumb:
            return self.thumb.height

    @property
    def size_thumb(self):
        if self.thumb:
            return filesizeformat(self.thumb.size)

    @property
    def width_thumb_sq(self):
        if self.thumb_sq:
            return self.thumb_sq.width

    @property
    def height_thumb_sq(self):
        if self.thumb_sq:
            return self.thumb_sq.height

    @property
    def size_thumb_sq(self):
        if self.thumb_sq:
            return filesizeformat(self.thumb_sq.size)

    def to_json(self):
        """Serialize an image"""

        data = {
            'src': f'{self.src.url}',
            'width': self.width,
            'height': self.height,
            'alt_text': self.alt_text or '',
        }

        if self.src_mobile:
            data['src_mobile'] = f'{self.src_mobile.url}'
            data['src_mobile_width'] = self.src_mobile.width
            data['src_mobile_height'] = self.src_mobile.height

        if self.thumb:
            data['thumb'] = f'{self.thumb.url}'
            data['thumb_width'] = self.thumb.width
            data['thumb_height'] = self.thumb.height

        if self.thumb_sq:
            data['thumb_sq'] = f'{self.thumb_sq.url}'
            data['thumb_sq_width'] = self.thumb_sq.width
            data['thumb_sq_height'] = self.thumb_sq.height

        return data

    def render_thumb_sq(self):
        return self._render(
            'core/components/img-square.html',
            context={'img': self, **self.to_json()}
        )

    def render(self):
        return self._render(
            'core/components/img.html',
            context={'img': self, **self.to_json()}
        )

    def deactivate(self):
        self.is_active = False
        self.save()


# Thumbnail
# Sizes


# class Thumbnail(RendererMixin, BaseModelMixin):
#     class Meta:
#         ordering = ('-updated', '-created')
#         verbose_name = _('Thumbnail')
#         verbose_name_plural = _('Thumbnails')

#     def __str__(self):
#         return f'{self.src}'

#     image = models.ForeignKey(
#         "core.Image",
#         verbose_name=_("Original Image"),
#         on_delete=models.CASCADE,
#         related_name='thumbnails'
#     )

#     src = models.ImageField(
#         max_length=500,
#         verbose_name="Thumbnail",
#         help_text="Select an image file",
#         upload_to=upload_thumb_to,
#         null=True, blank=True
#     )
#     is_square = models.BooleanField(default=False)
