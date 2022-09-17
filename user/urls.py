from django.urls import path, include
from user.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user"),


urlpatterns = [
    path("", include((router.urls, "user"), namespace="user")),
]
