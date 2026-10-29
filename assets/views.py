from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset
from django.shortcuts import get_object_or_404

def assets(request):
    lines = [f"{a.title}, {a.description}, {a.thumbnail.url if a.thumbnail else ''}, {a.file.url if a.file else ''}, {a.publisher}, {a.pk}" for a in Asset.objects.all()]
    
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def asset (request, asset_id):
    asset = get_object_or_404(Asset, asset_id=asset_id)
    
    return HttpResponse(f"{asset.title}, {asset.description}, {asset.thumbnail}, {asset.file}, {asset.publisher}, {asset.pk}")