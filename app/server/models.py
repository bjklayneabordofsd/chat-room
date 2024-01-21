from collections.abc import Iterable
from django.db import models
from django.conf import settings

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class ServerModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name="server_category")
    description = models.CharField(max_length=250, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

class ChannelModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(ServerModel, on_delete=models.CASCADE, related_name="channel_server")

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(ChannelModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name