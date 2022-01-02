

from io import BytesIO
# from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.parsers import JSONParser, MultiPartParser

from miq.utils import get_file_ext
from miq.utils import download_img_from_url, img_file_from_response
from miq.models import Section, Image, File

from miq.mixins import DevLoginRequiredMixin

from ..serializers import (
    # images
    ImageSerializer,

    # files
    FileSerializer,

    # sections
    SectionSerializer,
    get_section_serializer
)
from miq.auth import serializers

User = get_user_model()


"""
IMAGE
"""


class ImageViewset(DevLoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = ImageSerializer
    queryset = Image.objects.none()
    parser_classes = (JSONParser,  MultiPartParser)

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
                    # 'src': File(BytesIO(r.content), name=filename)
                }
            )

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data))

        # elif isinstance(data, list):
        #     serializer = self.get_serializer(data=request.data, many=True)

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        qs = Image.objects.active()\
            .user(self.request.user)\
            .site(get_current_site(self.request))
        return qs

    def perform_create(self, ser):
        ser.save(site=get_current_site(
            self.request), user=self.request.user)


"""
SECTION
"""


class SectionViewset(DevLoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    parser_classes = (JSONParser, )

    def get_queryset(self, *args, **kwargs):
        params = self.request.query_params

        if self.action == 'list':
            source = params.get('source')
            if not source or source == '':
                return Section.objects.none()

            source_type = params.get('source_type')
            if source_type == 'index':
                return Section.objects.filter(index__slug__in=[source])

            if source_type == 'page':
                return Section.objects.filter(pages__slug__in=[source])

            if source_type == 'post':
                return Section.objects.filter(posts__slug__in=[source])

            return Section.objects.filter(source=source)

        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            type = self.request.data.get('type')
            if not type:
                raise ValidationError({'type': 'Section type required.'})

            return get_section_serializer(type)

        return super().get_serializer_class()

    def perform_create(self, serializer):
        # TODO: Enforce
        serializer.save(site=get_current_site(self.request))


"""
# FILE
"""


class FileViewset(DevLoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = FileSerializer
    queryset = File.objects.all()
    parser_classes = (JSONParser,  MultiPartParser)

    def perform_create(self, ser):
        ser.save(site=get_current_site(
            self.request), user=self.request.user)
