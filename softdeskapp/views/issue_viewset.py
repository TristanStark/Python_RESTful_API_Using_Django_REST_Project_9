from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from ..models import  Issue, Project
from ..permissions import IsIssueProjectContributorAndAuthorForWrite
from ..serializers import IssueSerializer
from .helper import is_project_member

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [
        IsAuthenticated,
        IsIssueProjectContributorAndAuthorForWrite,
    ]

    def get_project(self):
        project_id = self.kwargs["project_pk"]
        project = get_object_or_404(Project, pk=project_id)

        if not is_project_member(self.request.user, project):
            raise PermissionDenied(
                "You must be a project contributor to access its issues."
            )

        return project

    def get_queryset(self):
        project = self.get_project()

        return Issue.objects.filter(project=project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def perform_create(self, serializer):
        project = self.get_project()
        assignee_user = serializer.validated_data.get("assignee_user")

        if assignee_user is None:
            assignee_user = self.request.user

        serializer.save(
            author_user=self.request.user,
            assignee_user=assignee_user,
            project=project,
        )

