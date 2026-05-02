from django.db import models

from apps.products.models import Product
from core.models import UUIDTimeStampedModel


class ProductPromotion(UUIDTimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="promotions",
    )
    title = models.CharField(max_length=255)
    boost_weight = models.PositiveSmallIntegerField(default=1)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        db_table = "ads_productpromotion"
