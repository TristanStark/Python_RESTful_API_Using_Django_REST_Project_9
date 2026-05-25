from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Contributor
from .user_serializers import UserSummarySerializer


User = get_user_model()


class ContributorSerializer(serializers.ModelSerializer):
    """Serialize project contributors.

    The API only accepts a user identifier when adding a contributor. The
    project, role and permission values are server-controlled, which prevents a
    caller from elevating privileges through mass assignment.
    """

    user = UserSummarySerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
    )
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "user_id",
            "project",
            "permission",
            "role",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "user",
            "project",
            "permission",
            "role",
            "created_time",
        ]
