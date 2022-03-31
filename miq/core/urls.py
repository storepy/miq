from django.urls import path, include
# from django.conf import settings

#from rest_framework import routers

from . import views

# from .auth import (
#     AccountUpdateViewset,
#     ImageViewset, SectionViewset, FileViewset
# )


app_name = 'core'

# auth_router = routers.DefaultRouter()

# auth_router.register(r'account', AccountUpdateViewset)
# auth_router.register(r'sections', SectionViewset)
# auth_router.register(r'images', ImageViewset)
# auth_router.register(r'files', FileViewset)

urlpatterns = [
    # API
    # path(f'{settings.API_PATH}/', include(auth_router.urls)),

    path('about/', views.AboutPage.as_view(), name='about'),
    path('<slug:slug>/', views.PageView.as_view(), name='page'),
]
