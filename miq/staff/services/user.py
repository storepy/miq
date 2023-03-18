
from django.contrib.auth import get_user_model

from rest_framework import serializers



User = get_user_model()


class UserSearchSerializer(serializers.Serializer):
    q = serializers.CharField(required=True, allow_blank=False, allow_null=False, min_length=3)

def user_search_qs(q):
    return User.objects.filter(is_active=True).search(q).order_by('-created')

