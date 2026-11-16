from .models import Asset, Favorite
from rest_framework import serializers
from django.conf import settings

class AssetSe(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['title', 'description', 'thumbnail', 'file', 'publisher', 'category', 'asset_id', 'created_at']
        read_only_fields = ["publisher"]

    def validate_file(self, value):
        if value and value.size > settings.MAX_ASSET_FILE_SIZE:
            raise serializers.ValidationError(
                f"File size must not exceed "
                f"{settings.MAX_ASSET_FILE_SIZE // (1024 * 1024)} MB."
            )
        return value

    def validate_thumbnail(self, value):
        if value and value.size > settings.MAX_THUMBNAIL_SIZE:
            raise serializers.ValidationError(
                f"Thumbnail size must not exceed "
                f"{settings.MAX_THUMBNAIL_SIZE // (1024 * 1024)} MB."
            )
        return value

from .models import Favorite

class FavoriteSe(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "asset", "created_at"]
        read_only_fields = ["id", "created_at"]