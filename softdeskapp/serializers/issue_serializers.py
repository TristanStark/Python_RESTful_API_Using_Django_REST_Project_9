from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Issue
from .user_serializers import UserSummarySerializer

User = get_user_model()


class IssueSerializer(serializers.ModelSerializer):
    author_user = UserSummarySerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    assignee_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "author_user",
            "assignee_user",
            "project",
            "priority",
            "tag",
            "status",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author_user",
            "project",
            "created_time",
        ]

    def validate_assignee_user(self, assignee_user):
        project = self.context.get("project")

        if assignee_user is None:
            return assignee_user

        if project and not project.contributors.filter(id=assignee_user.id).exists():
            raise serializers.ValidationError(
                "The assignee must be a contributor of the project."
            )

        return assignee_user

