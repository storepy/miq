from io import BytesIO
from PIL import Image

from django.db import transaction
from django.contrib.sites.models import Site
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import SimpleUploadedFile


@transaction.atomic
def get_or_create_site(*, is_live=False):
    if Site.objects.exists():
        site = Site.objects.first()
    else:
        site =  Site.objects.create()

    if is_live and not site.settings.is_live:
        s = site.settings
        s.is_live = True
        s.save()

    return site


def get_random_user_data():
    return {
        "first_name": get_random_string(10),
        "last_name": get_random_string(10),
        "username": get_random_string(10),
        "email": f"{get_random_string(10)}@{get_random_string(10)}.com",
        "password": get_random_string(10),
    }


def get_temp_img(size=50):
    bts = BytesIO()
    img = Image.new("RGB", (size, size))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())