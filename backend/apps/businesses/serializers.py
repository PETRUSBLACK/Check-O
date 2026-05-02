from rest_framework import serializers

from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ("id", "owner", "name", "slug", "status", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "status", "created_at", "updated_at")
