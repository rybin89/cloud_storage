from django.urls import path
from .views import LoginView,RegisterView,LogoutView

urlpatterns = [
    path('authorization/', LoginView.as_view(), name='authorization'),
    path('registration/', RegisterView.as_view(), name='authorization_success'),
    path('logout/', LogoutView.as_view(), name='logout'),
]