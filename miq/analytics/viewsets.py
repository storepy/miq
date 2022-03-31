from rest_framework import viewsets
# from rest_framework.parsers import JSONParser

from miq.mixins import StaffLoginRequired

from miqanalytics.models import Hit
from miqanalytics.staff.serializers import HitStaffSerializer


class HitStaffViewset(StaffLoginRequired, viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Hit.objects.all()
    serializer_class = HitStaffSerializer
