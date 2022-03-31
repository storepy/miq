from django.urls import path, include

urlpatterns = [
    path('', include('miqauth.urls', namespace='miqauth')),
    path('', include('miq.urls', namespace='miq')),
]
