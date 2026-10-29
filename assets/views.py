from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from .serializers import AssetSe
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsPublisherOrReadOnly

class Asset(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSe
    permission_classes = [IsAuthenticatedOrReadOnly, IsPublisherOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)