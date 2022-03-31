
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from ..models import User
from ..mixins import LoginRequiredMixin
from ..serializers import UserListSerializer


class SearchView(LoginRequiredMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none()
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self, *args, **kwargs):
        params = self.request.query_params
        q = params.get('q')
        if q and len(q) > 2:
            return User.objects.exclude(pk=self.request.user.pk)\
                .search(q)

        return self.queryset
