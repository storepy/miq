
from django.urls import path
from .views import PageView, IndexView

app_name = 'miq'

urlpatterns = [

    path('<slug:slug>/', PageView.as_view(), name='page'),
    path('', IndexView.as_view(), name='index'),
]
