from django.urls import path, include

urlpatterns = [
    path('', include('miq.urls', namespace='miq')),
    path('', include('miq.auth.accounts.urls', namespace='accounts')),
]
