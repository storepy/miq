
from miq.auth.serializers import ImageSerializer
from .user_ser import StaffUserSerializer


class StaffImageSerializer(ImageSerializer):
    class Meta(ImageSerializer.Meta):
        read_only_fields = (
            'slug', 'name', 'name_truncated', 'height', 'width', 'size',
            'user', 'created', 'updated',
        )
        fields = (
            'src', 'thumb', 'thumb_sq',
            'alt_text', 'caption', 'position',
            *read_only_fields
        )

    user = StaffUserSerializer(required=False)
