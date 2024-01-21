from django.contrib import admin

from .models import ChannelModel, ServerModel, CategoryModel

admin.site.register(ChannelModel)
admin.site.register(ServerModel)
admin.site.register(CategoryModel)
