from rest_framework import serializers

from miq.models import (
    Section, TextSection, MarkdownSection, ImageSection,
    Image
)

__all__ = (
    'SectionSerializer', 'ImageSectionSerializer',
    'MarkdownSectionSerializer', 'TextSectionSerializer'
)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'slug', 'title', 'type', 'text', 'url', 'html', 'position',
            'image', 'images', 'nodes',
            # 'images_data',
        )
        read_only_fields = ('slug', 'image')

    images = serializers.SlugRelatedField(
        slug_field='slug',
        # TODO: Filter active
        many=True, queryset=Image.objects.all(), required=False)


class ImageSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = ImageSection
        fields = ('slug', 'type', 'html', 'image', 'position',)


class MarkdownSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = MarkdownSection
        fields = (
            'slug', 'type', 'title', 'text',
            'html', 'position', 'nodes'
        )


class TextSectionSerializer(MarkdownSectionSerializer):
    class Meta(MarkdownSectionSerializer.Meta):
        model = TextSection
