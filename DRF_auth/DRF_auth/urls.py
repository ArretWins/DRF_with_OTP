from django.contrib import admin
from django.urls import path
from DRF_auth.accounts.views import RegisterAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('admin/', admin.site.urls),
]
