from miq.api_auth.serializers.user_ser import UserListSerializer
from rest_framework import serializers
from miq.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            'slug', 'src',
            'name_truncated', 'name', 'filename', 'ext', 'size', 'user',
            'created', 'updated',
        )
        read_only_fields = (
            'slug', 'name_truncated', 'name', 'filename', 'ext', 'size',
            'user', 'created', 'updated',
        )

    user = UserListSerializer(required=False)
    name = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    name_truncated = serializers.ReadOnlyField()
    ext = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()
