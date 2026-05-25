from rest_framework import serializers

from ..models import Comment
from .user_serializers import UserSummarySerializer



class CommentSerializer(serializers.ModelSerializer):
    author_user = UserSummarySerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "description",
            "author_user",
            "issue",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author_user",
            "issue",
            "created_time",
        ]