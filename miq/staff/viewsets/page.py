

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser


from miq.core.models import Page
from miq.core.permissions import DjangoModelPermissions


from ..mixins import LoginRequiredMixin
from ..serializers import PageSerializer, SectionSerializer


class PagePermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action == 'section':
            return request.user.has_perm('core.change_page')

        return super().has_permission(request, view)


class PagesActionMixin(LoginRequiredMixin):
    @action(methods=['post'], detail=True, url_path=r'section')
    def section(self, request, *args, **kwargs):
        """
        Add section to page
        """

        instance = self.get_object()
        serializer = SectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section = serializer.save(site=instance.site, source=instance.slug)
        instance.sections.add(section)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PageViewset(PagesActionMixin, viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    parser_classes = (JSONParser, )
    permission_classes = (IsAdminUser, PagePermissions)

    # def perform_create(self, serializer):
    #     # TODO: Enforce
    #     serializer.save(site=get_current_site(self.request))

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.parents()

        return qs
