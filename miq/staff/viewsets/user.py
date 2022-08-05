from django.apps import apps

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from ..models import User
from ..mixins import LoginRequiredMixin
from ..serializers import UserListSerializer, UserSerializer


class Mixin(LoginRequiredMixin):
    permission_classes = (IsAdminUser,)


class UserUpdateViewset(
        Mixin, mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet):

    lookup_field = 'slug'
    serializer_class = UserSerializer
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

        return self.retrieve(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     usr = self.get_object()
    #     UserSerializer(data=request.data).is_valid(raise_exception=True)
    #     usr.first_name = request.data.get('first_name')
    #     usr.last_name = request.data.get('last_name')
    #     usr.gender = request.data.get('gender')
    #     usr.save()

    #     return Response(UserSerializer(usr).data)

    def get_object(self):
        return self.request.user


class SearchView(Mixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none()
    serializer_class = UserListSerializer

    def get_queryset(self, *args, **kwargs):
        params = self.request.query_params
        q = params.get('q')
        if q and len(q) > 2:
            return User.objects\
                .exclude(pk=self.request.user.pk)\
                .search(q)

        return self.queryset
