from django.db import models

# from datetime import timedelta

# from django.db.models import DateTimeField, ExpressionWrapper, F, Count
# from django.utils import timezone
# from django.db.models.functions import TruncTime

from django.contrib.auth.models import UserManager as DjUserManager


from miq.core.models import UserQuerySet as MiqUserQuerySet


class UserQueryset(MiqUserQuerySet):
    pass


class UserManager(DjUserManager):
    def get_queryset(self, *args, **kwargs):
        return UserQueryset(self.model, *args, using=self._db, **kwargs)\
            .exclude(is_staff=False).select_related('img')
