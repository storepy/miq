from importlib.resources import path
import os
import subprocess
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Func, Value, Avg, F, Window, Count
from django.db.models.functions import Lower
from django.db.models.functions import StrIndex

from ...models import Hit


class Command(BaseCommand):
    help = 'Squash Hits'

    def handle(self, *args, **kwargs):
        qs = Hit.objects.all()\
            .exclude(path__icontains='/api')\
            .exclude(path__icontains='/shop/feed/')

        _qs = qs.values('created__date', 'ip').annotate(count=Count('ip'))\
            .order_by('-count')
        pprint([*_qs[:10]])

        import datetime
        dt = datetime.date(2022, 8, 9)
        qs = qs.filter(created__date=dt, path='/api/v1/carts/c8ab2afa-750e-4b93-aae0-21f8a1c15fa3/')
        print(qs.count())
        return

        by_count = qs.values('url', 'ip', 'referrer', 'user_agent', 'path')\
            .annotate(count=Count('url')).order_by('-count')

        qs = qs.annotate(
            avg_rating=Window(
                # expression=Avg('count'),
                expression=Count('url'),
                partition_by=[F('created__date')],
                # partition_by=[F('user_agent'), F('ip')],
                # order_by='url',
                # order_by=F('-created__date'),
            )).distinct().order_by('-created__date')

        pprint([*qs.values('avg_rating', 'url', 'ip', 'user_agent')[:5]])
        print(qs.count())
        # pprint(qs.values()[0])

        return

        print(by_count.count())

        sample = by_count[:50]

        d = OrderedDict()

        for h in sample.all():
            key = h.get('path')
            m = d.get(key) or []

            d[key] = [*m, h]

        for values in d.values():
            for hit_data in values:
                count = hit_data.pop('count', None)
                match = qs.filter(**hit_data).order_by('created')
                assert count == match.count()

                pprint([h for h in match.values_list('path', 'ip', 'url', 'user_agent')])
                # pprint([h['session_data'] for h in match.values()])

                # print(match.first().created, match.last().created)
                print()

            break
