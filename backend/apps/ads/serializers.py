from rest_framework import serializers

from .models import ProductPromotion


class ProductPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPromotion
        fields = (
            "id",
            "product",
            "title",
            "boost_weight",
            "starts_at",
            "ends_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
