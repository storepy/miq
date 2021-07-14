from django.urls import path

from . import LoginView

app_name = 'accounts'


urlpatterns = [
    # path('signup/', SignupView.as_view(), name='signup'),

    path('login/', LoginView.as_view(), name='login'),

    # path(
    #     'logout/',
    #     auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
    #     name='logout'),

]
