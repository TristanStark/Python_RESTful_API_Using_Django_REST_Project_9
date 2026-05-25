from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsIssueProjectContributorAndAuthorForWrite(BasePermission):
    """
    Allows issue access to project contributors.
    Update and delete are restricted to the issue author.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        project = obj.project

        is_project_member = (
            project.author_user == user
            or project.contributors.filter(id=user.id).exists()
        )

        if not is_project_member:
            return False

        if request.method in SAFE_METHODS:
            return True

        return obj.author_user == user
