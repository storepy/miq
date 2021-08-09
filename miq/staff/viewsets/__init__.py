from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser

from miq.models import Page, Index

from miq.mixins import DevLoginRequiredMixin
from miq.permissions import DjangoModelPermissions
from miq.auth import UserListSerializer, SectionSerializer

from ..serializers.page_ser import PageSerializer
from ..serializers.index_ser import IndexSerializer

User = get_user_model()


"""
PAGE
"""


class PagePermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action == 'section':
            return request.user.has_perm('miq.change_page')

        return super().has_permission(request, view)


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
    permission_classes = (IsAdminUser, PagePermissions)

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


class IndexPagePermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action == 'section':
            return request.user.has_perm('miq.change_index')

        return super().has_permission(request, view)


class IndexViewset(
        PagesActionMixin, mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    lookup_field = 'slug'
    serializer_class = IndexSerializer
    queryset = Index.objects.none()
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser, IndexPagePermissions)

    def get_object(self):
        site = get_current_site(self.request)
        return Index.objects.filter(site=site).first()


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
