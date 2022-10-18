from django.apps import apps
from django.conf import settings

# from django.utils.translation import gettext_lazy as _


from miq.core.views.generic import TemplateView


from .mixins import StaffViewMixin


class IndexView(StaffViewMixin, TemplateView):
    template_name = 'staff/base.django.html'
