
from django.contrib.auth import get_user_model

from rest_framework import serializers

from miq.models import File, Image
from miq.models import CloseTemplateSection, TextSection
from miq.models import Section, ImageSection, MarkdownSection, JumbotronSection

User = get_user_model()


"""
# IMAGE
"""


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'slug', 'src', 'thumb', 'thumb_sq',
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
# ACCOUNT
"""


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = (
            'slug', 'username', 'initials',
            'first_name', 'last_name', 'name',
            'img', 'img_data',
        )
        fields = read_only_fields

    initials = serializers.ReadOnlyField()
    name = serializers.SerializerMethodField()
    img = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.all(), required=False
    )
    img_data = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()

    def get_img_data(self, obj):
        if obj.img:
            return ImageSerializer(obj.img).data


class AccountSerializer(UserListSerializer):
    # Use in /accounts/account/

    class Meta(UserListSerializer.Meta):
        read_only_fields = ('username', 'slug', 'email')
        fields = (
            *read_only_fields,
            # 'username', 'slug', 'email',
            'first_name', 'last_name', 'name',
            'initials', 'gender', 'gender_label',
            'img', 'img_data',
            # 'birthdate', 'phone',
            # 'img', 'is_email_verified'
        )

    gender_label = serializers.ReadOnlyField()


"""
# SECTION
"""


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        read_only_fields = ('slug', 'image')
        fields = (
            *read_only_fields,
            'title', 'type', 'text', 'url', 'html', 'position',
            'images', 'nodes',
            # 'images_data',
        )

    image = ImageSerializer(required=False)
    images = serializers.SlugRelatedField(
        slug_field='slug',
        # TODO: Filter active
        many=True, queryset=Image.objects.all(), required=False)


"""
# JUMBOTRON SECTION
"""


class JumbotronSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = JumbotronSection
        read_only_fields = ('slug', 'image')
        fields = (
            *read_only_fields,
            'title', 'text', 'type',
            'html', 'position', 'images', 'url',
        )


"""
# IMAGE SECTION
"""


class ImageSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = ImageSection
        read_only_fields = ('slug',)
        fields = (*read_only_fields, 'type', 'html', 'image', 'position',)


"""
# MARKDOWN SECTION
"""


class MarkdownSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = MarkdownSection
        read_only_fields = ('slug',)
        fields = (
            *read_only_fields, 'type', 'title', 'text',
            'html', 'position', 'nodes'
        )


"""
# TEXT SECTION
"""


class TextSectionSerializer(MarkdownSectionSerializer):
    class Meta(MarkdownSectionSerializer.Meta):
        model = TextSection


"""
# CLOSE TEMPLATE SECTION
"""


class CloseTemplateSectionSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        model = CloseTemplateSection
        read_only_fields = ('slug',)
        fields = (
            *read_only_fields,
            'type', 'title', 'text',
            'html', 'image', 'images'
        )


"""

"""

sections_serializer_classes = {
    'IMG': ImageSectionSerializer,
    'TXT': TextSectionSerializer,
    'MD': MarkdownSectionSerializer,
    'JUMB': JumbotronSectionSerializer,
    'CLOSE': CloseTemplateSectionSerializer,
}


def get_section_serializer(type):
    return sections_serializer_classes.get(type.upper(), SectionSerializer)


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
