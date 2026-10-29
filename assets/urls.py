from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('assets/', views.assets, name='asset_list'),
    path('asset/<int:asset_id>', views.asset, name='asset'),
]
