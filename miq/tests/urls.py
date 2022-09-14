from django.urls import path, include

from miq.core.views import IndexView


urlpatterns = [

    path('', include('miq.analytics.urls', namespace='analytics')),
    path('', include('miq.staff.urls', namespace='staff')),
    path('', include('miq.core.urls', namespace='miq')),

    # path('', include('miq.auth.accounts.urls', namespace='accounts')),
    path('', IndexView.as_view(), name='index')
]
