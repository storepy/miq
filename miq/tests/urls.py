from django.urls import path, include

from miq.views import IndexView


urlpatterns = [
    path('', include('miq.urls', namespace='miq')),
    path('', include('miq.auth.accounts.urls', namespace='accounts')),
    path('', IndexView.as_view(), name='index')
]
