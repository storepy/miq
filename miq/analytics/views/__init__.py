
from django.apps import apps
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.translation import gettext_lazy as _


from ...core.views.generic import DetailView

# from ..models import LIB
# from ..serializers import LIBSerializer


class LIBView(DetailView):
    template_name = 'analytics/base.django.html'

    def get_object(self, *args, **kwargs):
        pass
        # return LIB.objects.get_or_create(name=self.kwargs.get('name'))[0]

    def get_context_data(self, **kwargs: dict):
        ctx = super().get_context_data(**kwargs)
        data = {}

        if apps.is_installed('shopy.store'):
            print('H+++>')

        self.update_sharedData(ctx, data)

        return ctx
