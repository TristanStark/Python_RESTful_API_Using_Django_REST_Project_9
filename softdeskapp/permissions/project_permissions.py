from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectContributorOrAuthor(BasePermission):
    """
    Allows project access only to the project author or contributors.
    Update and delete are restricted to the author.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        is_author = obj.author_user == user
        is_contributor = obj.contributors.filter(id=user.id).exists()

        if request.method in SAFE_METHODS:
            return is_author or is_contributor

        return is_author

