
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    short_bio = models.TextField(
        max_length=500,
        blank=True,
    )

    display_name = models.CharField(
        max_length=80,
        blank=True,
    )

    website = models.URLField(
        max_length=300,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def public_name(self):
        return self.display_name or self.user.username
