
from rest_framework import serializers

from ..models import Hit


class HitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        queryset = Hit.public.all()
        read_only_fields = (
            'slug', 'url', 'path', 'source_id', 'app', 'model', 'ip', 'session',
            'referrer', 'user_agent', 'method', 'response_status', 'debug', 'session_data',
            'created', 'updated'
        )
        fields = read_only_fields
