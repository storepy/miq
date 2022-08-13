# import logging


from django.db import models
# from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAdminUser

from ...staff.mixins import LoginRequiredMixin
from ...core.permissions import DjangoModelPermissions
from ...core.pagination import MiqPageNumberPagination

from ..models import Campaign, Hit, SearchTerm, LIB
from ..serializers import CampaignSerializer, CampaignSummarySerializer
from ..serializers import HitSerializer, SearchTermSerializer, LIBSerializer


class HitPagination(MiqPageNumberPagination):
    page_size = 100


class Mixin(LoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    parser_classes = (JSONParser, )
    pagination_class = HitPagination
    permission_classes = (IsAdminUser, DjangoModelPermissions)


class CampaignViewset(Mixin):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_serializer_class(self):
        if self.is_summary():
            return CampaignSummarySerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        # params = self.request.query_params
        if self.is_summary():
            qs = qs.values('key', 'value')\
                .annotate(count=models.Count('ip'))\
                .order_by('-count')

        return qs

    def is_summary(self) -> bool:
        return self.request.query_params.get('summary') == '1'


class SearchViewset(Mixin):
    queryset = SearchTerm.objects.all()
    serializer_class = SearchTermSerializer


class HitViewset(Mixin):
    queryset = Hit.public.all()
    serializer_class = HitSerializer

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
        data = qs.is_not_bot().exclude(method='OPTIONS')\
            .values('created__date', 'path',)\
            .annotate(count=models.Count('path'))\
            .order_by('-created__date', '-count')

        return Response(data=data)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if path := params.get('path'):
            qs = qs.filter(path=path)

        if ref := params.get('ref'):
            qs = qs.filter(referrer=ref)
        if ip := params.get('ip'):
            qs = qs.filter(ip=ip)

        if status := params.get('status'):
            qs = qs.filter(response_status=int(status))

        if ua := params.get('ua'):
            qs = qs.filter(user_agent=ua)

        bot = params.get('bot')
        if bot == '0':
            qs = qs.is_not_bot()
        if bot == '1':
            qs = qs.is_bot()

        path = params.get('path')
        if path and isinstance(path, str):
            qs = qs.filter(path__icontains=path)

        return qs


class LIBViewset(Mixin):
    queryset = LIB.objects.all()
    serializer_class = LIBSerializer
