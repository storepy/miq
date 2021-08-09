
from django.urls import path, re_path

from .views import StaffLoginView, AdminView


app_name = 'staff'


urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='login'),

    # Catch-all url
    re_path(r'', AdminView.as_view(), name='index'),
]
