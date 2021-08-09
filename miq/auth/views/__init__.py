from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from rest_framework.parsers import JSONParser, MultiPartParser

from miq.models import Image

from miq.mixins import DevLoginRequiredMixin

from ..serializers import (
    # images
    AccountSerializer, ImageSerializer, ImageSectionSerializer,

    # files
    FileSerializer,

    # sections
    SectionSerializer, TextSectionSerializer, MarkdownSectionSerializer,
)

User = get_user_model()


class AccountUpdateViewset(
        DevLoginRequiredMixin, mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'username'
    serializer_class = AccountSerializer
    queryset = User.objects.none()
    parser_classes = (JSONParser, )

    # @action(methods=['patch'], detail=True)
    # def profile(self, request, *args, **kwargs):
    #     serializer = ProfileSerializer(
    #         self.get_object().profile,
    #         data=request.data,
    #         partial=kwargs.pop('partial', False)
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return self.retrieve(request, *args, **kwargs)

    # @action(methods=['post', 'patch'], detail=True)
    # def avatar(self, request, *args, **kwargs):
    #     if request.method == 'PATCH':
    #         return self.retrieve(request, *args, **kwargs)

    #     serializer = ProfileSerializer(
    #         self.get_object().profile,
    #         data=request.data,
    #         partial=kwargs.pop('partial', False)
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
