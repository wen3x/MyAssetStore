from django.db import models
from config import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    thumbnail = models.ImageField(blank=True)
    file = models.FileField(blank=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="assets",
        null=True
    )

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "asset"],
                name="unique_user_asset_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.asset}"