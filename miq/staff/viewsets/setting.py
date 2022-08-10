from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import get_object_or_404

from ...core.models import SiteSetting

from ..mixins import LoginRequiredMixin
from ..serializers import SiteSettingSerializer, SiteSerializer, SiteSettingPagesSerializer


class SiteSettingViewsetMixin(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = SiteSetting.objects.none()
    parser_classes = (JSONParser,)
    permission_classes = (IsAdminUser, )

    def get_object(self):
        return get_object_or_404(SiteSetting, site=get_current_site(self.request))


class SiteSettingViewset(SiteSettingViewsetMixin):
    serializer_class = SiteSettingSerializer

    @action(methods=['patch'], detail=True)
    def config(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.config = {**obj.config, **request.data}
        obj.save()
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['patch'], detail=True)
    def pages(self, request, *args, **kwargs):
        ser = SiteSettingPagesSerializer(self.get_object(), data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()

        return self.retrieve(request, *args, **kwargs)

    @action(methods=['patch'], detail=True, url_path=r'site')
    def site(self, request, *args, **kwargs):
        # TODO: Validate domain(enforce ".")

        ser = SiteSerializer(
            self.get_object().site,
            data=request.data, partial=True
            # partial=kwargs.pop('partial', False)
        )
        if ser.is_valid(raise_exception=True):
            ser.save()

        return self.retrieve(request, *args, **kwargs)
