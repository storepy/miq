
from rest_framework import serializers

from miq.core.models import Image

from .image import ImageSerializer
from ..models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('slug', 'username', 'initials', 'is_staff', 'img',)
        fields = ('first_name', 'last_name', 'name', *read_only_fields)

    initials = serializers.ReadOnlyField()
    name = serializers.CharField(source='get_full_name', read_only=True)
    img = ImageSerializer(read_only=True)


class UserSerializer(UserListSerializer):
    class Meta(UserListSerializer.Meta):
        read_only_fields = (*UserListSerializer.Meta.read_only_fields, 'gender_label', 'img_data')
        fields = (
            'email', 'first_name', 'last_name', 'gender', 'img', *read_only_fields,
            # 'birthdate', 'phone',
            # 'img', 'is_email_verified'
        )

    gender_label = serializers.ReadOnlyField()
    img = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.all(), required=False
    )
    img_data = ImageSerializer(source="img", read_only=True)
