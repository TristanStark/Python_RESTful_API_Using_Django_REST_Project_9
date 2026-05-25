from django.urls import path

from .views import CommentViewSet, IssueViewSet, ProjectViewSet, SignupView

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
    path("projects/", project_list, name="project-list"),
    path("projects/<int:pk>/", project_detail, name="project-detail"),

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
    path("signup/", SignupView.as_view(), name="signup"),
]