# import logging

# import re
# from django.db.models import Q
# from pprint import pprint
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

from ..models import Hit, LIB
from ..serializers import HitSerializer, LIBSerializer


class HitPagination(MiqPageNumberPagination):
    page_size = 100


class Mixin(LoginRequiredMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    parser_classes = (JSONParser, )
    pagination_class = HitPagination
    permission_classes = (IsAdminUser, DjangoModelPermissions)


def get_hit_qs(request, *, qs=Hit.views.all()):
    params = request.query_params

    if params.get('__bot') == '1':
        qs = Hit.bots.all()

    if params.get('__err') == '1':
        qs = Hit.errors.all()

    if params.get('__public') == '1':
        qs = qs.is_public()

    if path := params.get('__path'):
        qs = qs.filter(path__icontains=path)
        if params.get('__exact') == '1':
            qs = qs.filter(path=path)

    if url := params.get('__url'):
        qs = qs.filter(url__icontains=url)
    if ref := params.get('__ref'):
        qs = qs.filter(referrer=ref)
    if ip := params.get('__ip'):
        qs = qs.filter(ip=ip)
    if params.get('__msg') == '1':
        # qs = qs.filter(response_status=302)
        qs = qs.filter(parsed_data__r='1')
        # parsed_data__r='1'

    if status := params.get('__status'):
        qs = qs.filter(response_status=int(status))
    if ua := params.get('__ua'):
        qs = qs.filter(user_agent=ua)

    return qs


class HitViewset(Mixin):
    queryset = Hit.views.all()
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
        data = qs.exclude(method='OPTIONS')\
            .values('created__date', 'path',)\
            .annotate(count=models.Count('path'))\
            .order_by('-created__date', '-count')

        return Response(data=data)

    def get_queryset(self):
        return get_hit_qs(self.request, qs=super().get_queryset())


class LIBViewset(Mixin):
    queryset = LIB.objects.all()
    serializer_class = LIBSerializer

    @action(methods=['get'], detail=True, url_path=r'hits')
    def hits(self, request, *args, **kwargs):
        obj = self.get_object()
        qs = get_hit_qs(
            self.request,
            qs=Hit.objects.filter(
                models.Q(path__icontains=f'{obj.name}')
                | models.Q(referrer__icontains=obj.name)
                | models.Q(parsed_data__utm_campaign=obj.name)
            ).distinct()
        )
        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = HitSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HitSerializer(queryset, many=True)
        return Response(serializer.data)


# name = 'tkshop'
# name = 'igshop'
# # name = 'profile'
# qs = Hit.objects.filter(
#     models.Q(path__icontains=name)
#     | models.Q(referrer__icontains=name)
#     | models.Q(parsed_data__utm_campaign=name)
# ).distinct()

# qs = Hit.objects.filter(
#     Q(user_agent__icontains='fb')
#     | Q(user_agent__icontains='ig')
#     | Q(user_agent__icontains='facebook')
#     | Q(user_agent__icontains='instagram')
# ).distinct()

# qs = Hit.objects.filter(user_agent__icontains='mobile').values(
#     'user_agent', 'parsed_data__is_mobile').annotate(c=models.Count('user_agent')).order_by('-c')

# print(qs.count(), qs.paths_by_ips().count(), qs.by_paths().count(), qs.by_uas().count())
# pprint(list(qs.by_uas())[:10])
# pprint(list(qs)[:10])

# u = 'mozilla/5.0 (android 10; mobile; rv:102.0) gecko/102.0 firefox/102.0'
# s = 'ip(hone|od)|android.+mobile|windows (ce|phone)|blackberry|bb10|symbian|webos|firefox.+fennec|opera m(ob|in)i|tizen.+mobile|polaris|iemobile|lgtelecom|nokia|sonyericsson|dolfin|uzard|natebrowser|ktf;|skt;'
# m = re.search(s, qs[10].get('user_agent'))
# print(m)

#
