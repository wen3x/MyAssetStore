from .models import Asset, Favorite
from rest_framework import serializers

class AssetSe(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['title', 'description', 'thumbnail', 'file', 'publisher', 'asset_id']
        read_only_fields = ["publisher"]

from .models import Favorite

class FavoriteSe(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "asset", "created_at"]
        read_only_fields = ["id", "created_at"]