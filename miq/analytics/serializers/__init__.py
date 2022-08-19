from django.apps import apps
from rest_framework import serializers

from ..models import Hit, LIB


class HitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        queryset = Hit.views.all()
        read_only_fields = (
            'slug', 'url', 'path', 'source_id', 'app', 'model', 'ip', 'session', 'parsed_data',
            'referrer', 'user_agent', 'method', 'response_status', 'debug', 'session_data',
            'created', 'updated',
            #
            'customer_data'

        )
        fields = read_only_fields

    customer_data = serializers.SerializerMethodField()

    def get_customer_data(self, obj):
        if apps.is_installed('shopy.sales') and (_cus := obj.session_data.get('_cus')):
            from shopy.sales.models import Customer
            from shopy.sales.serializers import CustomerSerializer

            try:
                return CustomerSerializer(
                    Customer.objects.filter(slug=_cus).first()
                ).data
            except Exception:
                return
        return


class LIBHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        queryset = Hit.objects.all()
        read_only_fields = ('slug', 'url', 'path', 'ip', 'referrer', 'user_agent', 'parsed_data')
        fields = read_only_fields


class LIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = LIB
        queryset = LIB.objects.all()
        read_only_fields = (
            'slug', 'utm_campaign',
            #  'hits', 'created', 'updated'
        )
        fields = (
            *read_only_fields,
            'name', 'utm_medium', 'utm_source', 'utm_content',
            # 'is_pinned',
        )

    utm_campaign = serializers.CharField(source='name', read_only=True)

    # hits = LIBHitSerializer(many=True, read_only=True)


# class CampaignSummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Campaign
#         queryset = Campaign.objects.all()
#         read_only_fields = ('key', 'value', 'count',)
#         fields = read_only_fields

#     count = serializers.IntegerField()


# class CampaignSerializer(CampaignSummarySerializer):
#     class Meta(CampaignSummarySerializer.Meta):
#         read_only_fields = ('slug', 'key', 'value', 'ip', 'created', 'updated')
#         fields = read_only_fields


# class SearchTermSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SearchTerm
#         queryset = SearchTerm.objects.all()
#         read_only_fields = ('slug', 'session', 'value', 'count', 'created', 'updated')
#         fields = read_only_fields
