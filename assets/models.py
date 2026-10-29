from django.db import models
from config import settings

class Asset(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    thumbnail = models.ImageField(blank=True)
    file = models.FileField(blank=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title