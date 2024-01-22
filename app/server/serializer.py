from rest_framework import serializers

from .models import CategoryModel, ServerModel, ChannelModel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelModel
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = ServerModel
        fields = "__all__"
