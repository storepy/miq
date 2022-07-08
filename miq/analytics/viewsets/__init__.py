# import logging

# from django.db import IntegrityError
# from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser

from miq.staff.mixins import LoginRequiredMixin
from miq.core.permissions import DjangoModelPermissions
from miq.core.pagination import MiqPageNumberPagination

from ..models import Hit
from ..serializers import HitSerializer


class HitPagination(MiqPageNumberPagination):
    page_size = 100


class HitViewset(LoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Hit.objects.all()
    serializer_class = HitSerializer
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    pagination_class = HitPagination
