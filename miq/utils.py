from django.apps import apps
from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.core.validators import validate_ipv46_address


def truncate_str(string: str, *, lenght: int = 80):
    return Truncator(string).chars(lenght)


def serialize_app_config(app_config):
    return {
        'label': app_config.label,
        'name': app_config.verbose_name,
        'models': [key for key in app_config.models.keys()]
    }


def get_serialized_app_configs_dict(exclude=None, exclude_django_apps=False):
    exclude = exclude if isinstance(exclude, list) else []
    if exclude_django_apps:
        exclude.extend([
            'admin', 'auth', 'contenttypes', 'messages',
            'sessions', 'sitemaps', 'sites', 'staticfiles'
        ])

    installed_apps = [
        serialize_app_config(app)
        for app in apps.get_app_configs()
    ]
    return {
        f"{app['label']}": app for app in installed_apps
        if f"{app['label']}" not in exclude
    }


def create_staffuser(username, password, **kwargs):
    """
    Creates a new user and sets is_staff to True
    """

    User = get_user_model()

    user = User.objects.create_user(username=username, **kwargs, is_staff=True)
    user.set_password(password)
    assert user.is_staff == True
    return user


def get_user_perms_list(user):
    return list(user.get_all_permissions())


def get_user_perms_dict(user):
    perms = get_user_perms_list(user)
    return {'count': len(perms), 'perms': perms}


def get_text_choices(TextChoiceModel):
    return [
        {'name': choice.name, 'label': choice.label, 'value': choice.value}
        for choice in TextChoiceModel
    ]


def get_ip(request):
    try:
        ip = request.META.get(
            'HTTP_X_FORWARDED_FOR',
            request.META.get('REMOTE_ADDR')
        )
        validate_ipv46_address(ip)
    except Exception:
        ip = None
    return ip
