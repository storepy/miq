# import logging

# from django.db import IntegrityError
# from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, serializers
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
    queryset = Hit.public.all()
    serializer_class = HitSerializer
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    pagination_class = HitPagination

    @action(methods=['post'], detail=False, url_path=r'batch')
    def batch(self, request, *args, **kwargs):
        data = request.data
        action = data.get('action')
        if not action:
            return serializers.ValidationError({'invalid': ''})

        slugs = data.get('slugs', [])
        hits = Hit.objects.filter(slug__in=slugs)
        if action == 'destroy' and hits.exists():
            hits.delete()
            return Response(data={'status': 'ok'})

        return Response(data={})

    @action(methods=['get'], detail=False, url_path=r'summary')
    def summary(self, request, *args, **kwargs):
        qs = self.get_queryset()
        today = qs.today()
        yst = qs.yesterday()
        data = {
            'today': {
                'count': today.is_not_bot().count(),
                'bots': today.is_bot().count()
            },
            'yesterday': {
                'count': yst.is_not_bot().count(),
                'bots': yst.is_bot().count()
            },
        }
        return Response(data=data)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        bot = params.get('bot')
        if bot == '0':
            qs = qs.is_not_bot()
        if bot == '1':
            qs = qs.is_bot()

        path = params.get('path')
        if path and isinstance(path, str):
            qs = qs.filter(path__icontains=path)

        return qs