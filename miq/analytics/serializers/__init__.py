
from rest_framework import serializers

from ..models import Campaign, Hit, SearchTerm


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


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        queryset = Campaign.objects.all()
        read_only_fields = ('slug', 'key', 'value', 'ip', 'created', 'updated')
        fields = read_only_fields


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        queryset = SearchTerm.objects.all()
        read_only_fields = ('slug', 'session', 'value', 'count', 'created', 'updated')
        fields = read_only_fields
