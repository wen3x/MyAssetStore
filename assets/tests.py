from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Asset, Category

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

    def test_pagination_structure_and_limits(self):
        for i in range(4):
            Asset.objects.create(
                publisher=self.wen3x,
                title=f"extra asset {i}",
                description="desc",
            )

        response = self.client.get(self.list_url, {"page_size": 2})
        self.assertEqual(response.status_code, 200)

        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIsNone(response.data["previous"])
        self.assertIsNotNone(response.data["next"])

    def test_pagination_second_page(self):
        for i in range(4):
            Asset.objects.create(
                publisher=self.wen3x,
                title=f"extra {i}",
                description="desc",
            )

        response = self.client.get(self.list_url, {"page": 2, "page_size": 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 2)

    def test_pagination_walk_by_next_link(self):
        for i in range(50):
            Asset.objects.create(
                publisher=self.wen3x,
                title=f"extra {i}",
                description="desc",
            )

        first = self.client.get(self.list_url)
        self.assertEqual(first.status_code, 200)

        if first.data["next"] is None:
            self.skipTest("Пагинация выключена или PAGE_SIZE слишком большой")

        second = self.client.get(first.data["next"])
        self.assertEqual(second.status_code, 200)
        self.assertIsNotNone(second.data["previous"])
        self.assertNotEqual(
            {a["asset_id"] for a in first.data["results"]},
            {a["asset_id"] for a in second.data["results"]},
        )

    def test_filter_by_publisher(self):
        Asset.objects.create(
            publisher=self.kent,
            title="kent asset",
            description="desc",
        )

        response = self.client.get(self.list_url, {"publisher": self.kent.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "kent asset")

        response_wen = self.client.get(self.list_url, {"publisher": self.wen3x.pk})
        self.assertEqual(response_wen.data["count"], 1)
        self.assertEqual(response_wen.data["results"][0]["title"], "wen3x asset")

    def test_filter_by_category(self):
        cat_a = Category.objects.create(name="Textures", slug="textures")
        cat_b = Category.objects.create(name="Models", slug="models")

        Asset.objects.create(
            publisher=self.wen3x,
            title="texture pack",
            description="desc",
            category=cat_a,
        )
        Asset.objects.create(
            publisher=self.wen3x,
            title="model pack",
            description="desc",
            category=cat_b,
        )

        response = self.client.get(self.list_url, {"category": cat_a.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "texture pack")

    def test_filter_existing_user_without_assets_returns_empty(self):
        loner = User.objects.create_user("loner", password="pass12345")

        response = self.client.get(self.list_url, {"publisher": loner.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_filter_nonexistent_publisher_returns_400(self):
        response = self.client.get(self.list_url, {"publisher": 999999})
        self.assertEqual(response.status_code, 400)
        self.assertIn("publisher", response.data)

    def test_search_by_partial_title(self):
        Asset.objects.create(
            publisher=self.kent,
            title="unique searchable title",
            description="desc",
        )
        response = self.client.get(self.list_url, {"search": "searchable"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "unique searchable title")

    def test_search_is_case_insensitive(self):
        Asset.objects.create(
            publisher=self.wen3x,
            title="UPPERCASE",
            description="desc",
        )
        response = self.client.get(self.list_url, {"search": "uppercase"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_no_match(self):
        response = self.client.get(self.list_url, {"search": "zzz_no_such_text"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)