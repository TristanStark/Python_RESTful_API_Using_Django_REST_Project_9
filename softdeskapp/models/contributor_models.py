from django.conf import settings
from django.db import models

from .project_models import Project


class Contributor(models.Model):
    class Permission(models.TextChoices):
        READ = "READ", "Read"
        WRITE = "WRITE", "Write"
        ADMIN = "ADMIN", "Admin"

    class Role(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CONTRIBUTOR = "CONTRIBUTOR", "Contributor"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_contributions",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_contributors",
    )

    permission = models.CharField(
        max_length=20,
        choices=Permission.choices,
        default=Permission.WRITE,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CONTRIBUTOR,
    )

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"],
                name="unique_user_project_contribution",
            )
        ]
        ordering = ["project", "user"]

    def __str__(self):
        return f"{self.user} -> {self.project} ({self.role})"