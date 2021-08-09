from rest_framework import serializers
from django.contrib.sites.models import Site
from django.urls import reverse_lazy


"""
ADMIN SITE SERIALIZER
"""


class AdminSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('name', 'domain', 'navbar')

    navbar = serializers.SerializerMethodField()

    def get_navbar(self, instance):
        return [
            {'label': 'Dashboard', 'path': reverse_lazy('staff:index')}
        ]
