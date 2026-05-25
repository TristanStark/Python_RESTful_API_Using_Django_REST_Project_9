from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    CommentViewSet,
    ContributorViewSet,
    IssueViewSet,
    ProjectViewSet,
    SignupView,
)

project_list = ProjectViewSet.as_view({
    "get": "list",
    "post": "create",
})

project_detail = ProjectViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

project_user_list = ContributorViewSet.as_view({
    "get": "list",
    "post": "create",
})

project_user_detail = ContributorViewSet.as_view({
    "delete": "destroy",
})

issue_list = IssueViewSet.as_view({
    "get": "list",
    "post": "create",
})

issue_detail = IssueViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

comment_list = CommentViewSet.as_view({
    "get": "list",
    "post": "create",
})

comment_detail = CommentViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),

    path("projects/", project_list, name="project-list"),
    path("projects/<int:pk>/", project_detail, name="project-detail"),

    path(
        "projects/<int:project_pk>/users/",
        project_user_list,
        name="project-user-list",
    ),
    path(
        "projects/<int:project_pk>/users/<int:user_pk>/",
        project_user_detail,
        name="project-user-detail",
    ),

    path(
        "projects/<int:project_pk>/issues/",
        issue_list,
        name="issue-list",
    ),
    path(
        "projects/<int:project_pk>/issues/<int:pk>/",
        issue_detail,
        name="issue-detail",
    ),

    path(
        "projects/<int:project_pk>/issues/<int:issue_pk>/comments/",
        comment_list,
        name="comment-list",
    ),
    path(
        "projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/",
        comment_detail,
        name="comment-detail",
    ),
]
