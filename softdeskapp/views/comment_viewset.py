from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from ..models import Comment, Issue, Project
from ..permissions import IsCommentProjectContributorAndAuthorForWrite
from ..serializers import CommentSerializer
from .helper import is_project_member

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsCommentProjectContributorAndAuthorForWrite,
    ]

    def get_project(self):
        project_id = self.kwargs["project_pk"]
        project = get_object_or_404(Project, pk=project_id)

        if not is_project_member(self.request.user, project):
            raise PermissionDenied(
                "You must be a project contributor to access comments."
            )

        return project

    def get_issue(self):
        project = self.get_project()
        issue_id = self.kwargs["issue_pk"]

        return get_object_or_404(
            Issue,
            pk=issue_id,
            project=project,
        )

    def get_queryset(self):
        issue = self.get_issue()

        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issue = self.get_issue()

        serializer.save(
            author_user=self.request.user,
            issue=issue,
        )
