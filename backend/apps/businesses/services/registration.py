from django.db import transaction

from apps.businesses.models import Business, BusinessStatus


def register_business(*, owner, name: str, slug: str) -> Business:
    with transaction.atomic():
        return Business.objects.create(
            owner=owner,
            name=name,
            slug=slug,
            status=BusinessStatus.PENDING,
        )


def set_business_status(*, business_id, status: BusinessStatus) -> Business:
    business = Business.objects.select_for_update().get(pk=business_id)
    business.status = status
    business.save(update_fields=["status", "updated_at"])
    return business
