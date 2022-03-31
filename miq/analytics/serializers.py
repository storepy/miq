from rest_framework import serializers

from miqanalytics.models import Hit


class HitStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        read_only_fields = (
            'slug',
            'source', 'session', 'path',
            'referrer', 'user_agent', 'ip', 'response_status',
            'debug',
            'created', 'updated'
        )
        fields = read_only_fields
