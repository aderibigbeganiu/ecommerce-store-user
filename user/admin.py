from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = (
        "email",
        "username",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "verified",
    )
    ordering = (
        "-date_joined",
        "verified",
    )
    list_display = ("username", "email", "country", "verified", "date_joined")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "slug",
                    "email",
                    "phone_number",
                    "username",
                    "first_name",
                    "last_name",
                    "country",
                    "password",
                    "verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        # ("Personal", {"fields": ("profile_picture",)}),
        ("Activity", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "verified",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
