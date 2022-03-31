
from rest_framework import serializers

from miq.core.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        read_only_fields = (
            'user', 'slug', 'name', 'name_truncated',
            'height', 'width', 'size',
            'height_mobile', 'width_mobile', 'size_mobile',
            'height_thumb', 'width_thumb', 'size_thumb',
            'height_thumb_sq', 'width_thumb_sq', 'size_thumb_sq',
            'created', 'updated',
        )
        fields = (
            'src', 'src_mobile', 'thumb', 'thumb_sq',
            'alt_text', 'caption', 'position',
            *read_only_fields
        )

    user = serializers.SlugRelatedField(slug_field="slug", read_only=True)
