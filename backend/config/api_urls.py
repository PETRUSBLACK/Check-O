from django.urls import include, path
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ads.api import ProductPromotionViewSet
from apps.analytics.api import AnalyticsEventViewSet
from apps.businesses.api import BusinessViewSet
from apps.delivery.api import ShipmentViewSet
from apps.notifications.api import NotificationViewSet
from apps.orders.api import OrderViewSet
from apps.payments.api import PaymentViewSet
from apps.products.api import ProductViewSet
from apps.subscriptions.api import VendorSubscriptionViewSet
from apps.users.api import UserViewSet
from apps.users.auth_api import MeView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"shipments", ShipmentViewSet, basename="shipment")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"subscriptions", VendorSubscriptionViewSet, basename="subscription")
router.register(r"promotions", ProductPromotionViewSet, basename="promotion")
router.register(r"analytics-events", AnalyticsEventViewSet, basename="analytics-event")


class HealthView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["system"],
        summary="Health check endpoint",
        responses={200: OpenApiResponse(description="API is healthy")},
    )
    def get(self, request):
        return Response({"status": "ok", "service": "smartmall-backend"})


urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("", include(router.urls)),
]
