from rest_framework import serializers
from apps import models


class PageSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"
