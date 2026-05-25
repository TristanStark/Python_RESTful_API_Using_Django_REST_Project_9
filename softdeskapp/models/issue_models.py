from django.conf import settings
from django.db import models
from .project_models import Project

class Issue(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Tag(models.TextChoices):
        BUG = "BUG", "Bug"
        ENHANCEMENT = "ENHANCEMENT", "Enhancement"
        TASK = "TASK", "Task"

    class Status(models.TextChoices):
        TODO = "TODO", "To-Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    title = models.CharField(max_length=255)
    description = models.TextField()

    tag = models.CharField(
        max_length=20,
        choices=Tag.choices,
        default=Tag.TASK,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )

    assignee_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title

