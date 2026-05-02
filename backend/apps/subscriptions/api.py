from rest_framework import permissions, viewsets

from apps.businesses.models import Business
from core.permissions import IsVendorOrAdmin

from .models import VendorSubscription
from .serializers import VendorSubscriptionSerializer


class VendorSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = VendorSubscription.objects.all()
    serializer_class = VendorSubscriptionSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsVendorOrAdmin()]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        qs = self.queryset.select_related("business", "plan")
        if user.is_staff or getattr(user, "role", None) == "admin":
            return qs.order_by("-created_at")
        ids = Business.objects.filter(owner=user).values_list("id", flat=True)
        return qs.filter(business_id__in=ids).order_by("-created_at")
