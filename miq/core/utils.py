from collections import namedtuple
import os
import requests
import logging
from io import BytesIO

from django.apps import apps
from django.utils import timezone
from django.core.files import File
# from django.urls.base import reverse_lazy
from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.core.validators import validate_ipv46_address

logger = logging.getLogger(__name__)
loginfo = logger.info
logerror = logger.error


def get_session(request):
    session = request.session
    if session.session_key:
        return session

    try:
        request.session.save()
        loginfo(f'New session[{request.session.session_key}]')
        return request.session
    except Exception as e:
        logerror(f'Cannot get session: {e}')


"""
FILES & IMAGES
"""


def get_image_files_path(instance):
    paths = [instance.src.path]
    if(field := instance.src_mobile):
        paths.append(field.path)
    if(field := instance.thumb_sq):
        paths.append(field.path)
    if(field := instance.thumb):
        paths.append(field.path)
    return paths


def clean_img_url(url: str) -> str:
    if url.startswith('//'):
        url = f'http://{url[2:]}'
    return url


def download_img_from_url(url, request=requests):
    url = clean_img_url(url)

    res = request.get(url)
    if res.status_code != 200:
        return None

    return res


def img_file_from_response(response, filename=None, ext='.jpg'):
    filename = filename or f'{timezone.now().timestamp()}{ext}'
    return File(BytesIO(response.content), name=filename)


def img_file_from_pil(pil_image, ext='png'):
    if not ext or ext.lower() not in ['webp', 'jpeg', 'png']:
        ext = 'png'

    blob = BytesIO()
    pil_image.save(blob, ext.upper())
    return File(blob)


def get_file_ext(path):
    return os.path.splitext(path)[1]


"""
STRING
"""


def truncate_str(string: str, *, length: int = 80):
    return Truncator(string).chars(length)


"""
APPS CONFIG
"""


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


"""
TESTS
"""


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


"""
MODELS
"""


def get_text_choices(TextChoiceModel):
    return [
        {'name': choice.name, 'label': choice.label, 'value': choice.value}
        for choice in TextChoiceModel
    ]


"""
HELPERS
"""


def get_dict_key(data: dict, key: str):
    if '__' not in key:
        return data.get(key)

    value = {**data}
    for key in key.split('__'):
        value = value.get(key, {})
    return value


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


def dict_to_tuple(name: str, data: dict):
    return namedtuple(name, [str(key) for key in data.keys()])
