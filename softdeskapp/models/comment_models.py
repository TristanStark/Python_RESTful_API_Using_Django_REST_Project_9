from django.conf import settings
from django.db import models

from .issue_models import Issue


class Comment(models.Model):
    description = models.TextField()

    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_comments",
    )

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"Comment #{self.pk} on issue #{self.issue_id}"