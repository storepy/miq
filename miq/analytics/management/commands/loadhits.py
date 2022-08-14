import json
from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand

from ...models import Hit


class Command(BaseCommand):
    help = 'Load Hits'

    def handle(self, *args, **kwargs):
        data = []
        with open('hits.json') as data_file:
            data = json.load(data_file)

        for h in data:
            hit = Hit.objects.create(**h)
            hit.created = parse_datetime(h.get('created'))
            hit.save()
            print(hit)
