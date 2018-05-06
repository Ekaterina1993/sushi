from django.urls import path

from . import views

urlpatterns = [
    path(r'signup/', views.signup, name='signup'),
    path(r'login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'profile/', views.profile, name='profile'),
    path(r'change_password/', views.change_password, name='change_password'),
]
