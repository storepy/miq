from django.db import models
from django.db.models import Value as V
# import datetime
from datetime import date
from django.db.models import Count

# from datetime import timedelta

# from django.db.models import DateTimeField, ExpressionWrapper, F, Count
# from django.utils import timezone
# from django.db.models.functions import TruncTime

from django.db.models.functions import Concat

from ...core.models import BaseManagerMixin


class DateQsMixin(BaseManagerMixin):

    def last_7_days(self):
        return self.get_last_n_days(7)

    def last_14_days(self):
        return self.get_last_n_days(14)

    def last_30_days(self):
        return self.get_last_n_days(30)

    def last_60_days(self):
        return self.get_last_n_days(60)

    def last_90_days(self):
        return self.get_last_n_days(90)

    def today(self):
        return self.created_today()

    def yesterday(self):
        return self.created_yesterday()


class AnalyticsMixin:
    def sent_message(self):
        return self.filter(parsed_data__r='1')

    def paths_by_ips(self):
        return self.values('path', 'ip').annotate(count=Count('ip')).order_by('-count')

    def by_paths(self):
        """
        Unique number of hits for each path by ip.
        """
        return self.values('path').annotate(count=Count('ip'))\
            .exclude(count=0).order_by('-count')

    def paths_count(self):
        """
        Total number of hits for each path.
        Similar to running self.filter(path='/path/name/').count()
        """
        return self.values('path')\
            .annotate(count=Count('path')).order_by('-count')

    def paths_by_uas(self):
        return self.values('path', 'user_agent').annotate(count=Count('user_agent'))\
            .order_by('-count')

    def count_by_created_date(self):
        return self.values('created__date').annotate(count=Count('ip'))\
            .order_by('-created__date')

    def by_ips(self):
        return self.values('ip').annotate(count=Count('ip'))\
            .order_by('-count')

    def by_uas(self):
        """ Group by user agents """
        return self.values('user_agent').annotate(count=Count('user_agent'))\
            .order_by('-count')


class LIBQueryset(DateQsMixin, models.QuerySet):
    def add_path(self):
        return self.annotate(
            path=Concat(V('/p/'), 'name', V('/'), output_field=models.SlugField())
        )


class LIBManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return LIBQueryset(self.model, *args, using=self._db, **kwargs)


class HitQueryset(DateQsMixin, AnalyticsMixin, models.QuerySet):

    def key_by_created_date(self, key: str, order_by='-created__date'):
        return self.values('created__date', 'path', key)\
            .annotate(count=Count(key))\
            .order_by('-count',).filter(created__date=date.today())

    def is_search(self):
        return self.filter(path__contains='?=')

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
        return self.exclude(is_bot=True)

    def is_bot(self):
        return self.filter(is_bot=True)

    def is_error(self):
        return self.filter(response_status__gt=299)

    def is_staff(self):
        return self.filter(path__icontains='/staff')

    def is_admin(self):
        return self.filter(path__icontains='/miq')

    def is_public(self):
        return self.exclude(pk__in=self.is_admin()).exclude(pk__in=self.is_staff())


class HitManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return HitQueryset(self.model, *args, using=self._db, **kwargs)


class ViewsManager(HitManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).is_not_bot()\
            .exclude(path__icontains='/api/v1')\



class BotsManager(HitManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).is_bot()


class ErrorsManager(HitManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).is_error()
