from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'slug', 'username', 'first_name', 'last_name', 'name', 'initials'
        )
        read_only_fields = fields

    initials = serializers.ReadOnlyField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()


class StaffUserSerializer(UserListSerializer):
    class Meta:
        model = User
        fields = (
            'slug', 'username',
            'first_name', 'last_name', 'name', 'initials',
            'email', 'is_staff'
        )