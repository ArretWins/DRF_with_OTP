from django.contrib import admin
from django.urls import path, include, re_path
from accounts.views import RegisterAPI, VerifyOTP, CustomLoginView, ShowApi, CustomLogoutView, DeleteProfileView
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'users', CustomLoginView)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('admin/', admin.site.urls),
    path('verify/', VerifyOTP.as_view(), name='verify-otp'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('logout/', CustomLogoutView.as_view(), name='custom-logout'),
    path('delete-profile/', DeleteProfileView, name='delete-profile'),
    path('', ShowApi.as_view(), name='user-list')
]