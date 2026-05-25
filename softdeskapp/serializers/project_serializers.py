from rest_framework import serializers

from ..models import Project
from .user_serializers import UserSummarySerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize projects without allowing client-side ownership changes.

    The project author is always set from the authenticated request user in
    ProjectViewSet.perform_create. Contributors are managed only through the
    dedicated contributor endpoints to avoid mass-assignment bypasses.
    """

    author_user = UserSummarySerializer(read_only=True)
    contributors = UserSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author_user",
            "contributors",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author_user",
            "contributors",
            "created_time",
        ]
