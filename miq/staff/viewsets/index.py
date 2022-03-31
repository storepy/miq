from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets, mixins
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser

from miq.core.models import Index
from miq.core.permissions import DjangoModelPermissions


from ..serializers import IndexSerializer

from .page import PagesActionMixin


class IndexPagePermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action == 'section':
            return request.user.has_perm('core.change_index')

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
