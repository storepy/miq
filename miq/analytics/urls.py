from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from . import viewsets


app_name = 'miqanalytics'


auth_router = routers.DefaultRouter()
auth_router.register(r'hits', viewsets.HitViewset)
auth_router.register(r'search', viewsets.SearchViewset)
auth_router.register(r'campaigns', viewsets.CampaignViewset)


urlpatterns = [
    path(f'{settings.API_PATH}/', include(auth_router.urls)),
]
