from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Contributor, Project
from ..serializers import ContributorSerializer
from .helper import is_project_member


class ContributorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Manage project collaborators.

    Routes:
    - GET /projects/{project_pk}/users/
    - POST /projects/{project_pk}/users/
    - DELETE /projects/{project_pk}/users/{user_pk}/
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_project(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        if not is_project_member(self.request.user, project):
            raise PermissionDenied(
                "You must be a project contributor to access this resource."
            )

        return project

    def check_project_author(self, project):
        if project.author_user_id != self.request.user.id:
            raise PermissionDenied(
                "Only the project author can manage project contributors."
            )

    def get_queryset(self):
        project = self.get_project()
        return (
            Contributor.objects
            .filter(project=project)
            .select_related("user", "project")
            .order_by("user__username")
        )

    def perform_create(self, serializer):
        project = self.get_project()
        self.check_project_author(project)

        user = serializer.validated_data["user"]

        if user == project.author_user:
            raise ValidationError(
                {"user_id": "The project author is already a project contributor."}
            )

        if Contributor.objects.filter(project=project, user=user).exists():
            raise ValidationError(
                {"user_id": "This user is already a contributor of this project."}
            )

        serializer.save(project=project)

    def destroy(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_project_author(project)

        user_id = self.kwargs["user_pk"]

        if int(user_id) == project.author_user_id:
            raise ValidationError(
                {"user_id": "The project author cannot be removed from contributors."}
            )

        contributor = get_object_or_404(
            Contributor,
            project=project,
            user_id=user_id,
        )
        contributor.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
