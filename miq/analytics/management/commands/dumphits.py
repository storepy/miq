import json

from django.core.management.base import BaseCommand

from rest_framework import serializers

from ...models import Hit


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        queryset = Hit.objects.all()
        fields = (
            'url', 'path', 'source_id', 'app', 'model', 'ip', 'session',
            'referrer', 'user_agent', 'method', 'response_status', 'debug', 'session_data',
            'created', 'updated')


class Command(BaseCommand):
    help = 'Dump Hits'

    def handle(self, *args, **kwargs):
        with open('hits.json', 'w', encoding='utf-8') as f:
            json.dump(Serializer(Hit.objects.all(), many=True).data, f, ensure_ascii=False, indent=4)
