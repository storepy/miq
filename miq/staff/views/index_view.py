from django.apps import apps
from django.conf import settings
from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site


from miq.core.views.generic import TemplateView
from miq.core.utils import get_user_perms_dict, get_serialized_app_configs_dict

from ..mixins import LoginRequiredMixin
from ..serializers import SiteSerializer, UserSerializer


class IndexView(LoginRequiredMixin, TemplateView):
    raise_exception = False
    permission_denied_message = ''
    login_url = reverse_lazy('staff:login')
    template_name = 'staff/base.django.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_current_site(self.request)

        data = {
            'site': SiteSerializer(site).data,
            'user': UserSerializer(self.request.user).data,
            'perms': get_user_perms_dict(self.request.user),
            'apps': get_serialized_app_configs_dict(
                exclude=['rest_framework'], exclude_django_apps=True
            )
        }

        # FBAPP
        if apps.is_installed('miqsocial'):
            context['fb_app_id'] = '5381519708543550'
            data['fb_app_id'] = '5381519708543550'

            if access_token := getattr(settings, 'FB_APP_ACCESS_TOKEN', None):
                data['fb_app_access_token'] = access_token

        # MIQHRM
        if apps.is_installed('miq_hrm'):
            Employee = apps.get_model('miq_hrm', 'Employee')

            employee = Employee.objects.filter(user=self.request.user)
            if employee.exists():
                employee = employee.first()
                data['user']['employee'] = employee.to_dict()

                company = employee.company
                data['company'] = {
                    'name': company.name,
                    'slug': company.slug
                }

        self.update_sharedData(context, data)

        return context
