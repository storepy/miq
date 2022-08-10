
from rest_framework import serializers

from ..models import Campaign, Hit, SearchTerm, LIB


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


class CampaignSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        queryset = Campaign.objects.all()
        read_only_fields = ('key', 'value', 'count',)
        fields = read_only_fields

    count = serializers.IntegerField()


class CampaignSerializer(CampaignSummarySerializer):
    class Meta(CampaignSummarySerializer.Meta):
        read_only_fields = ('slug', 'key', 'value', 'ip', 'created', 'updated')
        fields = read_only_fields


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        queryset = SearchTerm.objects.all()
        read_only_fields = ('slug', 'session', 'value', 'count', 'created', 'updated')
        fields = read_only_fields


class LIBHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        queryset = Hit.objects.all()
        read_only_fields = (
            'slug', 'url', 'path', 'source_id', 'ip', 'session',
            'referrer', 'user_agent', 'method', 'response_status', 'debug',
        )
        fields = read_only_fields


class LIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = LIB
        queryset = LIB.objects.all()
        read_only_fields = ('slug', 'utm_campaign', 'hits', 'created', 'updated')
        fields = (
            # *read_only_fields,
            'name', 'is_pinned',
            'utm_medium', 'utm_source', 'utm_content',
        )

    utm_campaign = serializers.CharField(source='name', read_only=True)

    hits = LIBHitSerializer(many=True, read_only=True)
