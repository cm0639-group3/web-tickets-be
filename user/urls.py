from django.urls import path, include
from . import views
from .views import UserRegisterView , UserLogoutView, UserChangePasswordView , UserProfileView, AllUsersProfileView, CreateAdminView

urlpatterns = [

    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserProfileView.as_view(), name='change_password'),
    path('allprofiles/', AllUsersProfileView.as_view(), name='user'),
    path('create_admin/', CreateAdminView.as_view(), name='create_admin'),


]
