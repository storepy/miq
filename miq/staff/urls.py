
from django.conf import settings
from django.urls import path, re_path, include

from rest_framework import routers

from . import views
from . import viewsets


app_name = 'staff'

staff_router = routers.DefaultRouter()

staff_router.register(r'account', viewsets.UserUpdateViewset)
staff_router.register(r'search-staff', viewsets.SearchView)

staff_router.register(r'pages', viewsets.PageViewset)
staff_router.register(r'index', viewsets.IndexViewset)
staff_router.register(r'staffimages', viewsets.ImageViewset, 'staffimage')
staff_router.register(r'settings', viewsets.SiteSettingViewset)


urlpatterns = [
    # API
    path(f'{settings.API_PATH}/', include(staff_router.urls)),

    path(f'{app_name}/login/', views.LoginView.as_view(), name='login'),

    # Catch-all url
    re_path(r'staff/', views.IndexView.as_view(), name='index'),
]
