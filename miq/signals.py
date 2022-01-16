import os

from django.dispatch import receiver
from django.db.models import signals
from django.contrib.sites.models import Site

from miq.models import Index, SiteSetting, Image
from miq.utils import get_image_files_path


# @receiver(signals.pre_save, sender=Site)
# def on_site_will_save(sender, instance, created, **kwargs):
#     if not Index.objects.filter(site=instance).exists():
#         Index.objects.create(site=instance, title="Welcome")

@receiver(signals.post_save, sender=Site)
def on_site_did_save(sender, instance, created, **kwargs):
    if not SiteSetting.objects.filter(site=instance).exists():
        SiteSetting.objects.create(site=instance,)

    if not Index.objects.filter(site=instance).exists():
        Index.objects.create(site=instance, title="Welcome")


@receiver(signals.post_delete, sender=Image)
def image_was_deleted(sender, instance, *args, **kwargs):
    for path in get_image_files_path(instance):
        if os.path.exists(path):
            os.remove(path)
