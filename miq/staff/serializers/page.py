from django.utils.text import slugify
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers

from miq.core.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        read_only_fields = (
            'slug', 'dt_published',
            'sections', 'children', 'updated_since',
        )
        fields = (
            # 'site',
            'slug_public', 'title', 'label', 'is_published',
            *read_only_fields,
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

    def validate_slug_public(self, value: str) -> str:
        return slugify(value)

    def create(self, validated_data):
        validated_data.update({'site': get_current_site(self.get_request())})
        return super().create(validated_data)

    def get_request(self):
        try:
            return self._kwargs.get('context').get('request')
        except Exception:
            return None
