
from django.apps import apps
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

from miq.auth.accounts import LoginView
from miq.views.generic import TemplateView
from miq.mixins import StaffLoginRequired
from miq.utils import get_user_perms_dict, get_serialized_app_configs_dict

from .forms import StaffAuthForm
from .serializers import AdminSiteSerializer
from .serializers.user_ser import StaffUserSerializer


"""
ADMIN VIEW
"""


class AdminViewMixin(StaffLoginRequired):

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

        if apps.is_installed('miq_hrm'):
            Employee = apps.get_model('miq_hrm', 'Employee')

            employee = Employee.objects.filter(user=self.request.user)
            if employee.exists():
                employee = employee.first()
                data['user']['employee'] = {
                    'slug': employee.slug,
                }

                company = employee.company
                data['company'] = {
                    'name': company.name,
                    'slug': company.slug
                }

        self.update_sharedData(context, data)

        return context


class AdminView(AdminViewMixin, TemplateView):
    login_url = reverse_lazy('staff:login')
    permission_denied_message = ''
    raise_exception = False


"""
LOGIN
"""


class StaffLoginView(LoginView):
    authentication_form = StaffAuthForm
    template_name = 'miq/staff/login.html'

    def get_redirect_url(self):
        return reverse_lazy('staff:index')
