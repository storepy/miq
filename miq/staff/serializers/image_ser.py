
from miq.auth.serializers import ImageSerializer
from .user_ser import StaffUserSerializer


class StaffImageSerializer(ImageSerializer):
    class Meta(ImageSerializer.Meta):
        read_only_fields = (
            'user', 'slug', 'name', 'name_truncated',
            'height', 'width', 'size',
            'height_mobile', 'width_mobile', 'size_mobile',
            'created', 'updated',
        )
        fields = (
            'src', 'src_mobile', 'thumb', 'thumb_sq',
            'alt_text', 'caption', 'position',
            *read_only_fields
        )

    user = StaffUserSerializer(required=False)
