
from django.contrib.auth import get_user_model

from .managers import UserManager


class User(get_user_model()):
    # user properties
    # username, first_name, last_name, email,
    # is_staff, is_active, date_joined
    # -- methods
    # get_full_name, get_short_name, email_user

    # user permission properties
    # groups, user_permissions
    # is_superuser
    # -- methods
    # get_user_permissions, get_group_permissions, get_all_permissions,
    # has_perm, has_perms, has_module_perms

    objects = UserManager()

    class Meta:
        proxy = True
