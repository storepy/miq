from uuid import uuid4

from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from .PATHS import PATHS

from . import views
# from . import viewsets

app_name = 'honeypot'


staff_router = routers.DefaultRouter()

# staff_router.register(r'logins', viewsets.LoginViewset)

urlpatterns = [
    path(f'{settings.API_PATH}/', include(staff_router.urls)),
    path('admin/login/', views.LoginAttemptView.as_view(), name='login'),
]

urlpatterns.extend([
    path(p, views.LoginAttemptView.as_view(), name=f'{uuid4()}') for p in PATHS
])
