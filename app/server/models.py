from collections.abc import Iterable
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension

def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"

def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"

def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path, 
        null=True, 
        blank=True,
        )
    
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(CategoryModel, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(CategoryModel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, send="server.CategoryModel")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
    
class ServerModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name="server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"{self.name}-{self.id}"

class ChannelModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(ServerModel, on_delete=models.CASCADE, related_name="channel_server")
    banner = models.ImageField(
        upload_to=server_banner_upload_path, 
        null=True, 
        blank=True, 
        validators=[validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path, 
        null=True, 
        blank=True, 
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(ServerModel, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(ServerModel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, send="server.ServerModel")
    def server_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
