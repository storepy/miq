
from django.apps import apps
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.translation import gettext_lazy as _


from ...core.views.generic import DetailView

from ..models import LIB


class LIBView(DetailView):
    template_name = 'analytics/base.django.html'

    def get_object(self, *args, **kwargs):
        return LIB.objects.get_or_create(name=self.kwargs.get('name'))[0]
