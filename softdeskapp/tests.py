from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from .models import Project

User = get_user_model()

class ProjectPermissionTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            password="password123",
        )
        self.contributor = User.objects.create_user(
            username="contributor",
            password="password123",
        )
        self.outsider = User.objects.create_user(
            username="outsider",
            password="password123",
        )

        self.project = Project.objects.create(
            title="Project",
            description="Description",
            type=Project.ProjectType.BACKEND,
            author_user=self.author,
        )
        self.project.contributors.add(self.author, self.contributor)

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

    def test_contributor_cannot_delete_project(self):
        self.client.force_authenticate(user=self.contributor)

        response = self.client.delete(f"/api/projects/{self.project.id}/")

        self.assertEqual(response.status_code, 403)