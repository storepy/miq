from django.dispatch import receiver
from django.db.models import signals
from django.contrib.sites.models import Site

from miq.models import Index, SiteSetting, JumbotronSection


# @receiver(signals.pre_save, sender=Site)
# def on_site_will_save(sender, instance, created, **kwargs):
#     if not Index.objects.filter(site=instance).exists():
#         Index.objects.create(site=instance, title="Welcome")

@receiver(signals.post_save, sender=Site)
def on_site_did_save(sender, instance, created, **kwargs):
    if not SiteSetting.objects.filter(site=instance).exists():
        SiteSetting.objects.create(
            site=instance,
            close_template=JumbotronSection.objects.create(site=instance)
        )

    if not Index.objects.filter(site=instance).exists():
        Index.objects.create(site=instance, title="Welcome")
