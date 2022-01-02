from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers

from miq.models import Page
from miq.mixins import ModelSerializerMixin


class PageSerializerMixin(ModelSerializerMixin, serializers.ModelSerializer):
    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True,
        # queryset=Section.objects.all(), required=False
    )


class PageSerializer(PageSerializerMixin):
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

    def create(self, validated_data):
        validated_data.update({'site': get_current_site(self.get_request())})
        return super().create(validated_data)
