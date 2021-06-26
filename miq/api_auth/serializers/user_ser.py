from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'slug', 'username', 'first_name', 'last_name', 'name'
        )
        read_only_fields = fields

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()
