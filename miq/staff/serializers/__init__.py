from rest_framework import serializers
from django.contrib.sites.models import Site
from django.urls import reverse_lazy

from miq.models import SiteSetting
from miq.auth.serializers import ImageSerializer
from miq.auth.serializers import CloseTemplateSectionSerializer
from miq.models.image_mod import Image
from .index_ser import IndexSerializer
from .page_ser import PageSerializer
from .user_ser import StaffUserSerializer
from .image_ser import StaffImageSerializer


__all__ = (
    'AdminSiteSerializer', 'AdminSiteSettingSerializer',
    'StaffUserSerializer', 'IndexSerializer', 'PageSerializer',
    'StaffImageSerializer'
)


"""
ADMIN SITE SERIALIZER
"""


class AdminSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        read_only_fields = ('navbar', 'settings')
        fields = ('name', 'domain', *read_only_fields)

    navbar = serializers.SerializerMethodField()
    settings = serializers.SlugRelatedField(
        slug_field="slug", read_only=True, required=False,
    )

    def get_navbar(self, instance):
        return [
            {'label': 'Dashboard', 'path': reverse_lazy('staff:index')}
        ]


class AdminSiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        read_only_fields = ('slug', 'site', 'close_template')
        fields = (
            'contact_email', 'is_live',
            'logo', 'logo_data',
            'ga_tracking', 'fb_pixel',
            *read_only_fields
        )

    site = AdminSiteSerializer(required=False)
    logo = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.active(),  required=False,)
    logo_data = serializers.SerializerMethodField()
    close_template = CloseTemplateSectionSerializer(required=False)

    def get_logo_data(self, instance):
        if (logo := instance.logo):
            return ImageSerializer(logo).data
        return None
