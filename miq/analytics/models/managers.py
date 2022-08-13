from django.db import models
import datetime
from datetime import date
from django.db.models import Count

# from datetime import timedelta

# from django.db.models import DateTimeField, ExpressionWrapper, F, Count
# from django.utils import timezone
# from django.db.models.functions import TruncTime


class HitQueryset(models.QuerySet):
    def key_by_created_date(self, key: str, order_by='-created__date'):
        return self.values('created__date', 'path', key)\
            .annotate(count=Count(key))\
            .order_by('-count',).filter(created__date=date.today())

    def is_search(self):
        return self.filter(path__contains='?=')

    def today(self):
        today = date.today()
        return self.filter(
            created__day=today.day, created__year=today.year,
            created__month=today.month).order_by('-created')

    def yesterday(self):
        yst = date.today() - datetime.timedelta(1)
        return self.filter(
            created__day=yst.day, created__year=yst.year,
            created__month=yst.month).order_by('-created')

    def social(self):
        # return self.get_queryset().filter(
        return self.filter(
            # models.Q(referrer__icontains='fb')
            # | models.Q(user_agent__icontains='fb')
            models.Q(user_agent__icontains='instagram')
            | models.Q(referrer__icontains='instagram')
        ).distinct()

    def external(self):
        return self.exclude(referrer__isnull=False)
        # .filter(referrer__icontains=domain_name)

    def is_not_bot(self):
        return self.exclude(pk__in=self.is_bot().values_list('pk', flat=True))

    def is_bot(self):
        return self.filter(
            models.Q(path__icontains='bot')
            | models.Q(user_agent__icontains='bot')
        ).distinct()


class HitManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return HitQueryset(self.model, *args, using=self._db, **kwargs)


class HitPublicManager(HitManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
            .exclude(path__startswith='/admin')\
            .exclude(path__icontains='/api/')
