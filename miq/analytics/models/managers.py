from django.db import models

# from datetime import timedelta

# from django.db.models import DateTimeField, ExpressionWrapper, F, Count
# from django.utils import timezone
# from django.db.models.functions import TruncTime


class HitQueryset(models.QuerySet):
    def is_search(self):
        return self.filter(path__contains='?=')


class HitManager(models.Manager):
    pass


class HitPublicManager(HitManager):
    def get_queryset(self, *args, **kwargs):
        super().get_queryset(*args, **kwargs).exclude(path__startswith='/admin')
