from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from . import views
from . import viewsets


app_name = 'miqanalytics'


auth_router = routers.DefaultRouter()
auth_router.register(r'hits', viewsets.HitViewset)
auth_router.register(r'libs', viewsets.LIBViewset)
auth_router.register(r'campaigns', viewsets.CampaignViewset)
auth_router.register(r'searchterms', viewsets.SearchViewset)


urlpatterns = [
    path('p/<slug:name>/', views.LIBView.as_view(), name='lib'),
    path(f'{settings.API_PATH}/', include(auth_router.urls)),
]
