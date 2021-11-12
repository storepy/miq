
from rest_framework import serializers

from miq.models import Image


class PublicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        read_only_fields = [
            'src', 'thumb', 'thumb_sq',
            'alt_text', 'caption', 'position',
            'name', 'name_truncated', 'height', 'width', 'size',
            'created', 'updated',
        ]
        fields = [*read_only_fields]

    name = serializers.ReadOnlyField()
    name_truncated = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()
