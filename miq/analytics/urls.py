from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from miqanalytics.staff import HitStaffViewset


app_name = 'miqanalytics'


auth_router = routers.DefaultRouter()
auth_router.register(r'hits', HitStaffViewset)


urlpatterns = [
    path(f'{settings.API_PATH}/', include(auth_router.urls)),
]
