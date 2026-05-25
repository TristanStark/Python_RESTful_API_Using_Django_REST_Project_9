from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Project
from ..permissions import IsProjectContributorOrAuthor
from ..serializers import ProjectSerializer



class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributorOrAuthor,
    ]

    def get_queryset(self):
        user = self.request.user

        return (
            Project.objects
            .filter(Q(author_user=user) | Q(contributors=user))
            .distinct()
        )

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)
        project.contributors.add(self.request.user)

