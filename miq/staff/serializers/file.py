
from rest_framework import serializers

from miq.core.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        read_only_fields = (
            'slug', 'name_truncated', 'name', 'filename', 'ext', 'size',
            'created', 'updated',
        )
        fields = ('src', *read_only_fields)
