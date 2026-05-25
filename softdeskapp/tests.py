from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Comment, Contributor, Issue, Project

User = get_user_model()


class OwaspPermissionTests(APITestCase):
    """Security tests for authentication, authorization and object ownership."""

    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="password123",
        )
        self.contributor = User.objects.create_user(
            username="contributor",
            email="contributor@example.com",
            password="password123",
        )
        self.other_contributor = User.objects.create_user(
            username="othercontributor",
            email="other@example.com",
            password="password123",
        )
        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        self.project = Project.objects.create(
            title="Project",
            description="Description",
            type=Project.ProjectType.BACKEND,
            author_user=self.author,
        )
        Contributor.objects.create(
            project=self.project,
            user=self.author,
            role=Contributor.Role.AUTHOR,
            permission=Contributor.Permission.ADMIN,
        )
        Contributor.objects.create(project=self.project, user=self.contributor)
        Contributor.objects.create(project=self.project, user=self.other_contributor)

        self.issue = Issue.objects.create(
            title="Issue",
            description="Issue description",
            project=self.project,
            author_user=self.contributor,
            assignee_user=self.contributor,
        )
        self.comment = Comment.objects.create(
            description="Comment description",
            issue=self.issue,
            author_user=self.contributor,
        )

    def test_anonymous_user_cannot_access_projects(self):
        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, 401)

    def test_author_can_read_project(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.get(f"/api/projects/{self.project.id}/")

        self.assertEqual(response.status_code, 200)

    def test_contributor_can_read_project(self):
        self.client.force_authenticate(user=self.contributor)

        response = self.client.get(f"/api/projects/{self.project.id}/")

        self.assertEqual(response.status_code, 200)

    def test_outsider_cannot_read_project(self):
        self.client.force_authenticate(user=self.outsider)

        response = self.client.get(f"/api/projects/{self.project.id}/")

        self.assertEqual(response.status_code, 404)

    def test_contributor_cannot_update_or_delete_project(self):
        self.client.force_authenticate(user=self.contributor)

        patch_response = self.client.patch(
            f"/api/projects/{self.project.id}/",
            {"title": "Forbidden update"},
            format="json",
        )
        delete_response = self.client.delete(f"/api/projects/{self.project.id}/")

        self.assertEqual(patch_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_project_create_does_not_mass_assign_contributors(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.post(
            "/api/projects/",
            {
                "title": "Mass assignment attempt",
                "description": "Should not add arbitrary contributors.",
                "type": Project.ProjectType.BACKEND,
                "contributors": [self.outsider.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(id=response.data["id"])
        self.assertFalse(project.contributors.filter(id=self.outsider.id).exists())
        self.assertTrue(project.contributors.filter(id=self.author.id).exists())

    def test_author_can_add_contributor_without_role_escalation(self):
        self.client.force_authenticate(user=self.author)
        candidate = User.objects.create_user(
            username="candidate",
            email="candidate@example.com",
            password="password123",
        )

        response = self.client.post(
            f"/api/projects/{self.project.id}/users/",
            {
                "user_id": candidate.id,
                "role": Contributor.Role.AUTHOR,
                "permission": Contributor.Permission.ADMIN,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        contributor = Contributor.objects.get(project=self.project, user=candidate)
        self.assertEqual(contributor.role, Contributor.Role.CONTRIBUTOR)
        self.assertEqual(contributor.permission, Contributor.Permission.WRITE)

    def test_only_project_author_can_manage_contributors(self):
        self.client.force_authenticate(user=self.contributor)

        response = self.client.post(
            f"/api/projects/{self.project.id}/users/",
            {"user_id": self.outsider.id},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_project_contributor_can_read_issue_but_not_update_or_delete_it(self):
        self.client.force_authenticate(user=self.other_contributor)

        get_response = self.client.get(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/"
        )
        patch_response = self.client.patch(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/",
            {"title": "Forbidden issue update"},
            format="json",
        )
        delete_response = self.client.delete(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/"
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_project_contributor_can_read_comment_but_not_update_or_delete_it(self):
        self.client.force_authenticate(user=self.other_contributor)
        url = (
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/"
            f"comments/{self.comment.id}/"
        )

        get_response = self.client.get(url)
        patch_response = self.client.patch(
            url,
            {"description": "Forbidden comment update"},
            format="json",
        )
        delete_response = self.client.delete(url)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_outsider_cannot_access_nested_issue_or_comment(self):
        self.client.force_authenticate(user=self.outsider)

        issue_response = self.client.get(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/"
        )
        comment_response = self.client.get(
            f"/api/projects/{self.project.id}/issues/{self.issue.id}/"
            f"comments/{self.comment.id}/"
        )

        self.assertEqual(issue_response.status_code, 403)
        self.assertEqual(comment_response.status_code, 403)
