from rest_framework import serializers
from django.contrib.sites.models import Site
from django.urls import reverse_lazy

from miq.models import SiteSetting
from miq.auth.serializers import JumbotronSectionSerializer
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
            'ga_tracking', 'fb_pixel',
            *read_only_fields
        )

    site = AdminSiteSerializer(required=False)
    close_template = JumbotronSectionSerializer(required=False)
