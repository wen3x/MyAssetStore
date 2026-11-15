from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, mixins
from .serializers import AssetSe
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsPublisherOrReadOnly
from .models import Favorite
from .serializers import FavoriteSe
from .pagination import AssetPa
from rest_framework.filters import SearchFilter, DjangoFilterBackend

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSe
    pagination_class = AssetPa
    permission_classes = [IsAuthenticatedOrReadOnly, IsPublisherOrReadOnly,]

    filterset_fields = ["category", "publisher"]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet ):
    serializer_class = FavoriteSe
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)