from django.urls import path, include
from django.conf import settings


from rest_framework import routers

from .views import PageView
from .auth import (
    AccountUpdateViewset,
    ImageViewset, SectionViewset, FileViewset
)
from .staff import (
    PageViewset, IndexViewset, StaffSearchView
)

app_name = 'miq'

auth_router = routers.DefaultRouter()
auth_router.register(r'search-staff', StaffSearchView)

auth_router.register(r'account', AccountUpdateViewset)
auth_router.register(r'pages', PageViewset)
auth_router.register(r'sections', SectionViewset)
auth_router.register(r'index', IndexViewset)
auth_router.register(r'images', ImageViewset)
auth_router.register(r'files', FileViewset)

urlpatterns = [
    path('<slug:slug>/', PageView.as_view(), name='page'),

    # API
    path(f'{settings.API_PATH}/', include(auth_router.urls)),
]
