from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import Project
from .user_serializers import UserSummarySerializer

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    author_user = UserSummarySerializer(read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

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
            "created_time",
        ]
