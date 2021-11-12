from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from miq.models import Image
from miq.mixins import StaffLoginRequired

from miq.staff.serializers import StaffImageSerializer

"""
IMAGE
"""


class StaffImageViewset(StaffLoginRequired, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = StaffImageSerializer
    queryset = Image.objects.none()
    parser_classes = (JSONParser,  MultiPartParser)

    def get_queryset(self):
        qs = Image.objects.all().site(get_current_site(self.request))
        return qs

    def perform_create(self, ser):
        ser.save(site=get_current_site(self.request), user=self.request.user)
