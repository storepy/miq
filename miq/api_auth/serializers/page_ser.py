from rest_framework import serializers

from miq.models import (
    Page, Section
)

__all__ = (
    'PageSerializer',
)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'slug', 'children', 'sections', 'label',  'is_published', 'dt_published',
            'updated_since',
            # 'sections_data',
        )
        read_only_fields = ('dt_published', 'sections', 'children')

    updated_since = serializers.ReadOnlyField()

    children = serializers.SlugRelatedField(
        slug_field="slug", read_only=True, many=True
    )
    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True,
        # queryset=Section.objects.all(), required=False
    )
