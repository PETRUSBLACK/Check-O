from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class BusinessStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending review"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    SUSPENDED = "suspended", "Suspended"


class Business(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=BusinessStatus.choices,
        default=BusinessStatus.DRAFT,
    )
    legal_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Registered legal name for verification.",
    )
    registration_number = models.CharField(
        max_length=128,
        blank=True,
        help_text="Business / company registration number.",
    )
    tax_identifier = models.CharField(
        max_length=64,
        blank=True,
        help_text="Tax ID / VAT where applicable.",
    )
    business_phone = models.CharField(max_length=32, blank=True)
    address = models.TextField(blank=True)
    submitted_for_review_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = "businesses_business"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
