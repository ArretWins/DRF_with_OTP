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
    # path('login/', CustomLoginView.as_view(), name = 'login'),
    # path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('logout/', CustomLogoutView, name='custom-logout'),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', ShowApi.as_view())
]