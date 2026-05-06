from uuid import UUID

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from apps.delivery.models import DeliveryMode, Shipment, ShipmentStatus
from apps.orders.models import OrderStatus


def _notify_user_shipment(*, user_id, payload: dict) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {"type": "notify", "payload": payload},
    )


_ALLOWED_SHIPMENT_TRANSITIONS = {
    ShipmentStatus.PENDING.value: {ShipmentStatus.PROCESSING.value},
    ShipmentStatus.PROCESSING.value: {ShipmentStatus.PACKAGING.value},
    ShipmentStatus.PACKAGING.value: {ShipmentStatus.PICKUP.value},
    ShipmentStatus.PICKUP.value: {ShipmentStatus.IN_TRANSIT.value},
    ShipmentStatus.IN_TRANSIT.value: {ShipmentStatus.DELIVERED.value},
    ShipmentStatus.DELIVERED.value: set(),
}


@transaction.atomic
def create_shipment(
    *,
    order_id: UUID,
    mode: str,
    partner: str = "",
    tracking_number: str = "",
) -> Shipment:
    from apps.orders.models import Order

    order = Order.objects.select_for_update().get(pk=order_id)
    if order.status not in (OrderStatus.PAID.value, OrderStatus.PROCESSING.value):
        raise ValueError("shipment can only be created for paid/processing orders")
    return Shipment.objects.create(
        order_id=order_id,
        mode=mode,
        partner=partner if mode == DeliveryMode.PARTNER else "",
        tracking_number=tracking_number,
        status=ShipmentStatus.PENDING,
    )


@transaction.atomic
def update_shipment_status(*, shipment_id: UUID, status: str) -> Shipment:
    shipment = Shipment.objects.select_for_update().select_related("order").get(pk=shipment_id)
    valid = {c.value for c in ShipmentStatus}
    if status not in valid:
        raise ValueError("invalid shipment status")
    if shipment.status == status:
        return shipment
    allowed = _ALLOWED_SHIPMENT_TRANSITIONS.get(shipment.status, set())
    if status not in allowed:
        raise ValueError(f"invalid shipment transition from {shipment.status} to {status}")
    shipment.status = status
    shipment.save(update_fields=["status", "updated_at"])
    customer_id = shipment.order.customer_id
    _notify_user_shipment(
        user_id=customer_id,
        payload={
            "kind": "delivery_update",
            "shipment_id": str(shipment.id),
            "status": shipment.status,
            "tracking_number": shipment.tracking_number,
        },
    )
    return shipment
