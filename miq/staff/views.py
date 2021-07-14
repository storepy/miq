
from django.contrib.sites.shortcuts import get_current_site

from miq.auth.accounts import LoginView
from miq.views.generic import TemplateView
from miq.mixins import DevLoginRequiredMixin
from miq.utils import get_user_perms_dict, get_serialized_app_configs_dict

from .forms import StaffAuthForm
from .api.serializers import AdminSiteSerializer, StaffUserSerializer


"""
ADMIN VIEW
"""


class AdminViewMixin(DevLoginRequiredMixin):
    template_name = 'miq/staff/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_current_site(self.request)

        data = {
            'site': AdminSiteSerializer(site).data,
            'user': StaffUserSerializer(self.request.user).data,
            'perms': get_user_perms_dict(self.request.user),
            'apps': get_serialized_app_configs_dict(
                exclude=['rest_framework'], exclude_django_apps=True
            )
        }

        self.update_sharedData(context, data)

        return context


class AdminView(AdminViewMixin, TemplateView):
    pass


"""
LOGIN
"""


class StaffLoginView(LoginView):
    authentication_form = StaffAuthForm
    template_name = 'miq/staff/login.html'
