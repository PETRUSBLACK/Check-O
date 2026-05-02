from django.db import models

from apps.businesses.models import Business
from core.models import TimeStampedModel, UUIDTimeStampedModel


class SubscriptionPlan(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price_monthly = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "subscriptions_plan"


class VendorSubscription(UUIDTimeStampedModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="vendor_subscriptions",
    )
    active = models.BooleanField(default=True)
    renews_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "subscriptions_vendorsubscription"
