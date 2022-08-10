
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.response import Response
from rest_framework import viewsets, status, serializers
from rest_framework.parsers import JSONParser, MultiPartParser

from miq.core.models import Image, File
from miq.core.utils import get_file_ext
from miq.core.utils import download_img_from_url, img_file_from_response

from ..mixins import LoginRequiredMixin
from ..serializers import ImageSerializer, FileSerializer

"""
IMAGE
"""


class ImageViewset(LoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Image.objects.none()
    parser_classes = (JSONParser, MultiPartParser)
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        src = data.get('src')
        if isinstance(src, str):
            res = download_img_from_url(src)
            if not res:
                raise serializers.ValidationError(
                    {'submit': _('Invalid action')})

            serializer = self.get_serializer(
                data={
                    'alt_text': data.get('alt_text', ''),
                    'src': img_file_from_response(res, None, get_file_ext(src))
                }
            )

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data))

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        qs = Image.objects.all().site(get_current_site(self.request))
        return qs

    def perform_create(self, ser):
        ser.save(site=get_current_site(self.request), user=self.request.user)


class FileViewset(LoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = File.objects.none()
    parser_classes = (JSONParser, MultiPartParser)
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all().site(get_current_site(self.request))

    def perform_create(self, ser):
        ser.save(site=get_current_site(self.request), user=self.request.user)
