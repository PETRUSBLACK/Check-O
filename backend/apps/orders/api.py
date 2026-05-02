from uuid import UUID

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.orders.models import Order
from apps.orders.serializers import OrderCreateSerializer, OrderSerializer
from apps.orders.services.order_service import (
    OrderFlowError,
    create_order_with_lines,
    transition_order_status,
)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        qs = self.queryset.prefetch_related("items__product")
        if user.is_staff or getattr(user, "role", None) == "admin":
            return qs.order_by("-created_at")
        return qs.filter(customer=user).order_by("-created_at")

    @extend_schema(
        request=OrderCreateSerializer,
        responses={201: OrderSerializer},
        tags=["orders"],
        summary="Create order with line items",
    )
    def create(self, request, *args, **kwargs):
        ser = OrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            order = create_order_with_lines(
                customer=request.user,
                lines=ser.validated_data["items"],
            )
        except OrderFlowError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(OrderSerializer(order).data)
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["post"], url_path="transition")
    @extend_schema(
        request=None,
        responses={200: OrderSerializer},
        tags=["orders"],
        summary="Transition order status",
        description="POST body must include `status` string.",
    )
    def transition(self, request, pk=None):
        to_status = request.data.get("status")
        if not to_status:
            return Response({"detail": "status required"}, status=400)
        order = self.get_object()
        if order.customer_id != request.user.id and not request.user.is_staff:
            return Response(status=403)
        try:
            transition_order_status(order_id=UUID(str(pk)), to_status=to_status)
        except OrderFlowError as e:
            return Response({"detail": str(e)}, status=400)
        order.refresh_from_db()
        return Response(OrderSerializer(order).data)
