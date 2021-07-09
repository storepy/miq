from rest_framework import serializers

from miq.models import File, Image
from miq.models import Section, ImageSection, MarkdownSection, TextSection
from miq.staff.api.serializers.user_ser import UserListSerializer


"""
# SECTION
"""


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


"""
# IMAGE SECTION
"""


class ImageSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = ImageSection
        fields = ('slug', 'type', 'html', 'image', 'position',)


"""
# MARKDOWN SECTION
"""


class MarkdownSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = MarkdownSection
        fields = (
            'slug', 'type', 'title', 'text',
            'html', 'position', 'nodes'
        )


"""
# TEXT SECTION
"""


class TextSectionSerializer(MarkdownSectionSerializer):
    class Meta(MarkdownSectionSerializer.Meta):
        model = TextSection


"""
# IMAGE
"""


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'slug', 'src',
            'alt_text', 'caption', 'position',
            'name', 'name_truncated', 'height', 'width', 'size',
            'created', 'updated',
        )
        read_only_fields = (
            'slug', 'name', 'name_truncated', 'height', 'width', 'size',
            'created', 'updated',
        )

    name = serializers.ReadOnlyField()
    name_truncated = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()


"""
# FILE
"""


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            'slug', 'src',
            'name_truncated', 'name', 'filename', 'ext', 'size', 'user',
            'created', 'updated',
        )
        read_only_fields = (
            'slug', 'name_truncated', 'name', 'filename', 'ext', 'size',
            'user', 'created', 'updated',
        )

    user = UserListSerializer(required=False)
    name = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    name_truncated = serializers.ReadOnlyField()
    ext = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()
