from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Asset

User = get_user_model()

class AssetApiTest(APITestCase):
    def setUp(self):
        self.wen3x = User.objects.create_user("wen3x", password="pass12345")
        self.kent = User.objects.create_user("kent", password="pass12345")
        self.asset = Asset.objects.create(
            publisher=self.wen3x, title="wen3x asset", description="desc"
        )
        self.list_url = reverse("asset-list")
        self.detail_url = reverse("asset-detail", args=[self.asset.pk])

    def test_user_can_create_and_becomes_publisher(self):
        self.client.force_authenticate(user=self.kent)
        payload = {"title": "kent asset", "description": "desc"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        created = Asset.objects.get(title="kent asset")
        self.assertEqual(created.publisher, self.kent)

    def test_owner_can_edit(self):
        self.client.force_authenticate(user=self.wen3x)
        response = self.client.patch(self.detail_url, {"title": "new"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.title, "new")

    def test_anonymous_can_read(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_cannot_create(self):
        payload = {"title": "x", "description": "desc"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertIn(response.status_code, (401, 403))

    def test_other_user_cannot_edit(self):
        self.client.force_authenticate(user=self.kent)
        response = self.client.patch(self.detail_url, {"title": "hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.title, "wen3x asset")

    def test_other_user_cannot_delete(self):
        self.client.force_authenticate(user=self.kent)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Asset.objects.filter(pk=self.asset.pk).exists())