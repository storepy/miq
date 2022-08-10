
from django.urls import reverse_lazy
from django.contrib.sites.models import Site

from rest_framework import serializers

from miq.core.models import SiteSetting, Image, File


from .file import FileSerializer
from .image import ImageSerializer


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        read_only_fields = ('navbar', 'settings')
        fields = ('name', 'domain', *read_only_fields)

    navbar = serializers.SerializerMethodField()
    settings = serializers.SlugRelatedField(slug_field="slug", read_only=True,)

    def get_navbar(self, instance):
        return [
            {'label': 'Dashboard', 'path': reverse_lazy('staff:index')}
        ]


class CloseTemplateSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        read_only_fields = ('slug',)
        fields = (
            'ct_title', 'ct_text', 'ct_html', 'ct_image',
            *read_only_fields
        )


class SiteSettingPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        read_only_fields = ('slug',)
        fields = (
            'about', 'about_html', 'faq', 'faq_html',
            'terms', 'terms_html', 'privacy', 'privacy_html',
            *read_only_fields
        )


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        read_only_fields = ('slug', 'site', 'logo_data', 'ico_data', 'ct_image_data', 'config')
        fields = (
            'is_live', 'logo', 'ico',
            'contact_number', 'contact_number_title', 'contact_number_display',
            'contact_email', 'whatsapp_number', 'whatsapp_link', 'whatsapp_link_title',
            'ga_tracking', 'fb_pixel', 'fb_app_id', 'fb_app_secret',

            *CloseTemplateSettingSerializer.Meta.fields,
            *SiteSettingPagesSerializer.Meta.fields,
            *read_only_fields
        )

    site = SiteSerializer(required=False)
    ico = serializers.SlugRelatedField(
        slug_field="slug", queryset=File.objects.all(), required=False,)
    ico_data = FileSerializer(source='ico', read_only=True)

    logo = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.active(), required=False,)
    logo_data = ImageSerializer(source='logo', read_only=True)

    ct_image = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.active(), required=False,)
    ct_image_data = ImageSerializer(source='ct_image', read_only=True)
