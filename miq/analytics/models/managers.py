from django.db import models

# from datetime import timedelta

# from django.db.models import DateTimeField, ExpressionWrapper, F, Count
# from django.utils import timezone
# from django.db.models.functions import TruncTime


class HitQueryset(models.QuerySet):
    pass


class HitManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return HitQueryset(self.model, using='analytics')
