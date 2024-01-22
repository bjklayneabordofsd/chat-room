from rest_framework import serializers

from .models import CategoryModel, ServerModel

class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerModel
        fields = "__all__"
