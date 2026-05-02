from django.db import models

from apps.businesses.models import Business
from core.models import TimeStampedModel


class Product(TimeStampedModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "products_product"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
