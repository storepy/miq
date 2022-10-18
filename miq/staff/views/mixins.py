from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

from miq.core.utils import get_user_perms_dict, get_serialized_app_configs_dict

from ..mixins import LoginRequiredMixin
from ..serializers import SiteSerializer, UserSerializer


class StaffViewMixin(LoginRequiredMixin):
    raise_exception = False
    permission_denied_message = ''
    login_url = reverse_lazy('staff:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'site': SiteSerializer(get_current_site(self.request)).data,
            'user': UserSerializer(self.request.user).data,
            'perms': get_user_perms_dict(self.request.user),
            'apps': get_serialized_app_configs_dict(exclude=['rest_framework'], exclude_django_apps=True)
        }

        self.update_sharedData(context, data)

        return context
