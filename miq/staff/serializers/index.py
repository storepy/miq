

from rest_framework import serializers

from miq.core.models import Index, Image

from .image import ImageSerializer


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        read_only_fields = ('slug', 'sections', 'cover_data')
        fields = (*read_only_fields, 'title', 'cover')

    cover = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.all(), required=False
    )
    cover_data = ImageSerializer(source='cover', read_only=True)
    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True, required=False,
    )
