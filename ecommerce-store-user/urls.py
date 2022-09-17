from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("allauth.urls")),
]
