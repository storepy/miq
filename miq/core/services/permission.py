from django.contrib.auth.models import Permission


def perm_get(codename) -> Permission:
    return Permission.objects.get(codename=codename)