"""Payment gateway adapters (Flutterwave, Paystack, Stripe) plug in here."""

from decimal import Decimal
from uuid import UUID

from django.db import transaction

from apps.orders.models import OrderStatus
from apps.orders.services.order_service import transition_order_status
from apps.payments.models import Payment, PaymentProvider, PaymentStatus

_VALID_PROVIDERS = {c.value for c in PaymentProvider}


@transaction.atomic
def initiate_payment(
    *,
    order_id: UUID,
    provider: str,
    amount: Decimal,
    external_ref: str = "",
) -> Payment:
    if provider not in _VALID_PROVIDERS:
        raise ValueError("invalid provider")
    payment = Payment.objects.create(
        order_id=order_id,
        provider=provider,
        amount=amount,
        external_ref=external_ref,
        status=PaymentStatus.PENDING,
    )
    return payment


@transaction.atomic
def confirm_payment_success(*, payment_id: UUID) -> Payment:
    payment = Payment.objects.select_for_update().select_related("order").get(pk=payment_id)
    payment.status = PaymentStatus.SUCCESS
    payment.save(update_fields=["status", "updated_at"])
    transition_order_status(order_id=payment.order_id, to_status=OrderStatus.PAID.value)
    return payment
