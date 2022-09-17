from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

import environ

env = environ.Env()

COUNTRY_CHOICES = [
    ("NG", "Nigeria"),
    ("GH", "Ghana"),
    ("KE", "Kenya"),
    ("UG", "Uganda"),
    ("TZ", "Tanzania"),
    ("ZA", "South Africa"),
]


def upload_to(instance, fileame):
    return f'{env("UPLOAD_USER_PICTURE")}/{instance.username}/{fileame}'


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")
        return self.create_user(email, username, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    slug = models.SlugField(blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_regex = RegexValidator(
        regex=r"\+\d{14}$",
        message="Phone number must be entered in the format: '+2348012345678'. A '+' and up to 14 digits allowed.",
    )
    phone_number = models.CharField(
        # validators=[phone_regex],
        max_length=15,
        unique=True,
        null=True,
    )
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    # profile_picture = models.ImageField(
    #     default="user_images/default_profile_picture_sk4yqh.jpg", upload_to=upload_to
    # )
    verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)

        super(User, self).save(*args, **kwargs)
