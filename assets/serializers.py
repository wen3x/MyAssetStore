from .models import Asset
from rest_framework import serializers

class AssetSe(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['title', 'description', 'thumbnail', 'file', 'publisher', 'asset_id']