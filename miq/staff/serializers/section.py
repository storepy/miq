

from rest_framework import serializers

from miq.core.models import Section, Image

from .image import ImageSerializer


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        read_only_fields = ('slug', 'image', 'images_data',)
        fields = (
            *read_only_fields,
            'title', 'type', 'text', 'url', 'html', 'position',
            'images',
            'nodes',
        )

    image = ImageSerializer(required=False)
    images = serializers.SlugRelatedField(
        slug_field='slug',
        # TODO: Filter active
        many=True, queryset=Image.objects.all(), required=False)
    images_data = serializers.SerializerMethodField()

    def get_images_data(self, instance):
        if instance.images.exists():
            return ImageSerializer(
                instance.images.order_by('created'), many=True
            ).data
        return []
