from rest_framework import serializers

from miq.models import Index, Image
from .image_ser import StaffImageSerializer


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        read_only_fields = ('slug', 'sections', 'cover_data')
        fields = (*read_only_fields, 'title', 'cover')

    cover = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.all(), required=False
    )
    cover_data = serializers.SerializerMethodField(required=False)
    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True, required=False,
    )

    def get_cover_data(self, obj):
        if not obj.cover:
            return
        return StaffImageSerializer(obj.cover).data
