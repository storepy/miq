from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ValidationError
from rest_framework.parsers import JSONParser, MultiPartParser

from miq.models import Section, Page, Index, Image, File

from miq.mixins import DevLoginRequiredMixin

from .serializers import (
    # images
    ImageSerializer, ImageSectionSerializer,

    # files
    FileSerializer,

    # sections
    SectionSerializer, TextSectionSerializer, MarkdownSectionSerializer,
    PageSerializer, IndexSerializer,

    # user
    UserListSerializer
)

User = get_user_model()


"""
IMAGE
"""


class ImageViewset(DevLoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = ImageSerializer
    queryset = Image.objects.none()
    parser_classes = (JSONParser,  MultiPartParser)

    def get_queryset(self):
        qs = Image.objects.active().site(get_current_site(self.request))
        return qs

    def perform_create(self, ser):
        ser.save(site=get_current_site(self.request), user=self.request.user)


"""
SECTION
"""

sections_serializer_classes = {
    'IMG': ImageSectionSerializer,
    'TXT': TextSectionSerializer,
    'MD': MarkdownSectionSerializer,
}


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

            return Section.objects.filter(source=source)

        return super().get_queryset(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            type = self.request.data.get('type')
            if not type:
                raise ValidationError({'type': 'Section type required.'})

            if type in sections_serializer_classes.keys():
                return sections_serializer_classes.get(type)

        return super().get_serializer_class()

    def perform_create(self, serializer):
        # TODO: Enforce
        serializer.save(site=get_current_site(self.request))


"""
PAGE
"""


class PagesActionMixin(DevLoginRequiredMixin):
    @action(methods=['post'], detail=True, url_path=r'section')
    def section(self, request, *args, **kwargs):
        """
        Add section to page
        """

        instance = self.get_object()

        serializer = SectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section = serializer.save(site=instance.site, source=instance.slug)
        instance.sections.add(section)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PageViewset(PagesActionMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        # TODO: Enforce
        serializer.save(site=get_current_site(self.request))

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.parents()

        return qs


"""
INDEX PAGE
"""


class IndexViewset(
        PagesActionMixin, mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    lookup_field = 'slug'
    serializer_class = IndexSerializer
    queryset = Index.objects.none()
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser,)

    def get_object(self):
        site = get_current_site(self.request)
        return Index.objects.filter(site=site).first()


"""
# FILE
"""


class FileViewset(DevLoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = FileSerializer
    queryset = File.objects.all()
    parser_classes = (JSONParser,  MultiPartParser)

    def perform_create(self, ser):
        ser.save(site=get_current_site(self.request), user=self.request.user)


"""
# USER
"""


class StaffSearchView(
        DevLoginRequiredMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none()
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self, *args, **kwargs):
        params = self.request.query_params
        q = params.get('q')
        if q and len(q) > 2:
            return User.objects.staff()\
                .exclude(pk=self.request.user.pk)\
                .search(q)

        return self.queryset
