from rest_framework import serializers

from .models import VendorSubscription


class VendorSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorSubscription
        fields = (
            "id",
            "business",
            "plan",
            "active",
            "renews_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
