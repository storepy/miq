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
    def today(self):
        self.created_today()

    def yesterday(self):
        self.created_yesterday()


class LIBQueryset(DateQsMixin, models.QuerySet):
    def add_path(self):
        return self.annotate(
            path=Concat(V('/p/'), 'name', V('/'), output_field=models.SlugField())
        )

    def with_hits(self):
        from miq.analytics.models import Hit
        libQs = self.add_path()

        print(libQs.values_list('name', flat=True))
        qs = Hit.objects.filter(
            # models.Q(path__in=libQs.values_list('path', flat=True))
            # |libQs.values_list('name', flat=True)
            models.Q(session_data__query__utm_campaign__contains__in=['igshop', 'catly', 'cataly', 'cata', 'analy'])
            # models.Q(session_data__query__utm_campaign__contains=['cataly'])

            # | models.Q(session_data__query__utm_campaign__in=libQs.values_list('name', flat=True))
        ).distinct()
        print(qs.count())
        # print(qs[0])
        return self


class LIBManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return LIBQueryset(self.model, *args, using=self._db, **kwargs)


class HitQueryset(DateQsMixin, models.QuerySet):

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
