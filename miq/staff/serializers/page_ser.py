from rest_framework import serializers

from miq.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        read_only_fields = ('dt_published', 'sections', 'children')
        fields = (
            *read_only_fields,
            'slug_public', 'slug',
            'label', 'is_published',
            'updated_since',
            # 'sections_data',
        )

    updated_since = serializers.ReadOnlyField()
    children = serializers.SlugRelatedField(
        slug_field="slug", read_only=True, many=True
    )
    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True,
        # queryset=Section.objects.all(), required=False
    )
