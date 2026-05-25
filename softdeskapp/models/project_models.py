from django.conf import settings
from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "BACKEND", "Back-end"
        FRONTEND = "FRONTEND", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=ProjectType.choices,
    )

    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="softdeskapp.Contributor",
        related_name="contributed_projects",
        blank=True,
    )

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title
