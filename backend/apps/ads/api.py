from rest_framework import permissions, viewsets

from apps.businesses.models import Business
from core.permissions import IsVendorOrAdmin

from .models import ProductPromotion
from .serializers import ProductPromotionSerializer


class ProductPromotionViewSet(viewsets.ModelViewSet):
    queryset = ProductPromotion.objects.all()
    serializer_class = ProductPromotionSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsVendorOrAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        qs = self.queryset.select_related("product__business")
        user = self.request.user
        if self.action in ("list", "retrieve"):
            return qs.order_by("-starts_at")
        if user.is_staff or getattr(user, "role", None) == "admin":
            return qs.order_by("-starts_at")
        ids = Business.objects.filter(owner=user).values_list("id", flat=True)
        return qs.filter(product__business_id__in=ids).order_by("-starts_at")
