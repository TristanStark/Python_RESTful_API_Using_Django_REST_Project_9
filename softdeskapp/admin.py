from django.contrib import admin

from .models import Comment, Issue, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "type",
        "author_user",
        "created_time",
    ]
    search_fields = [
        "title",
        "description",
    ]
    list_filter = [
        "type",
        "created_time",
    ]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "project",
        "author_user",
        "assignee_user",
        "priority",
        "tag",
        "status",
        "created_time",
    ]
    list_filter = [
        "priority",
        "tag",
        "status",
        "created_time",
    ]
    search_fields = [
        "title",
        "description",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "issue",
        "author_user",
        "created_time",
    ]
    search_fields = [
        "description",
    ]