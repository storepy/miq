
from django.urls import path, re_path

from miq.staff.views import StaffLoginView, AdminView


app_name = 'staff'


urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='login'),

    # Catch-all url
    re_path(r'', AdminView.as_view(), name='index'),
]
