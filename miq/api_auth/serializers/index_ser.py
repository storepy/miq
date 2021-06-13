from rest_framework import serializers

from miq.models import (
    Index
)

__all__ = ('IndexSerializer',)

fields = ('slug', 'title', 'sections',)


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = fields
        read_only_fields = ('slug', 'sections')

    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True, required=False,
    )
