from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from . import views
from . import viewsets


app_name = 'miqanalytics'


auth_router = routers.DefaultRouter()
auth_router.register(r'hits', viewsets.HitViewset)
auth_router.register(r'landings', viewsets.LandingViewset)
auth_router.register(r'campaigns', viewsets.CampaignViewset)
auth_router.register(r'searchterms', viewsets.SearchViewset)


urlpatterns = [
    path('p/<slug:name>/', views.LandingView.as_view(), name='landing'),
    path(f'{settings.API_PATH}/', include(auth_router.urls)),
]
