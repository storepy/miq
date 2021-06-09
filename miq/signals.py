from django.dispatch import receiver
from django.db.models import signals
from django.contrib.sites.models import Site

from miq.models import Index


@receiver(signals.post_save, sender=Site)
def on_site_did_save(sender, instance, created, **kwargs):
    if not Index.objects.filter(site=instance).exists():
        Index.objects.create(site=instance, title="Welcome")
