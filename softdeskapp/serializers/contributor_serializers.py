from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Contributor
from .user_serializers import UserSummarySerializer


User = get_user_model()


class ContributorSerializer(serializers.ModelSerializer):
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
            "created_time",
        ]
