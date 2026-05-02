from decimal import Decimal
from typing import Iterable
from uuid import UUID

from django.db import transaction

from apps.orders.models import Order, OrderItem, OrderStatus
from apps.products.models import Product


class OrderFlowError(Exception):
    pass


def _lines_from_payload(lines: Iterable[dict]) -> list[tuple[UUID, int]]:
    out: list[tuple[UUID, int]] = []
    for row in lines:
        out.append((UUID(str(row["product_id"])), int(row["quantity"])))
    return out


@transaction.atomic
def create_order_with_lines(*, customer, lines: Iterable[dict]) -> Order:
    parsed = _lines_from_payload(lines)
    order = Order.objects.create(
        customer=customer,
        status=OrderStatus.PENDING_PAYMENT,
        total=Decimal("0.00"),
    )
    total = Decimal("0.00")
    for product_id, qty in parsed:
        product = Product.objects.select_for_update().select_related("business").get(
            pk=product_id
        )
        if not product.is_active or product.business.status != "approved":
            raise OrderFlowError("Product not available")
        if product.stock < qty:
            raise OrderFlowError("Insufficient stock")
        line_total = product.price * qty
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            unit_price=product.price,
        )
        total += line_total
        product.stock -= qty
        product.save(update_fields=["stock", "updated_at"])
    order.total = total
    order.save(update_fields=["total", "updated_at"])
    return order


@transaction.atomic
def transition_order_status(*, order_id: UUID, to_status: str) -> Order:
    order = Order.objects.select_for_update().get(pk=order_id)
    valid = {c.value for c in OrderStatus}
    if to_status not in valid:
        raise OrderFlowError("Invalid status")
    order.status = to_status
    order.save(update_fields=["status", "updated_at"])
    return order
