from django.contrib import admin
from django.urls import path, include, re_path
from accounts.views import RegisterAPI, VerifyOTP, CustomLoginView, ShowApi, CustomLogoutView
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'users', CustomLoginView)

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('admin/', admin.site.urls),
    path('verify/', VerifyOTP.as_view()),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('logout/', CustomLogoutView, name='custom-logout'),
    path('', ShowApi.as_view())
]