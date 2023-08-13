from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterAPI, VerifyOTP, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('admin/', admin.site.urls),
    path('verify/', VerifyOTP.as_view())
]
