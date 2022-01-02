from django.apps import apps
from django.contrib.auth import get_user_model
# from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from miq.mixins import DevLoginRequiredMixin

from ..serializers import (
    # images
    AccountSerializer
)

User = get_user_model()


class AccountUpdateViewset(
        DevLoginRequiredMixin, mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'username'
    serializer_class = AccountSerializer
    queryset = User.objects.none()
    parser_classes = (JSONParser, )

    @action(methods=['patch'], detail=True, url_path=r'position')
    def employee_position(self, request, *args, **kwargs):
        if apps.is_installed('miq_hrm'):
            Employee = apps.get_model('miq_hrm', 'Employee')

            employee = Employee.objects.filter(user=self.request.user)
            if employee.exists():
                employee = employee.first()
                employee.position = request.data.get('position')
                employee.save()

            print(employee.position)

        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
