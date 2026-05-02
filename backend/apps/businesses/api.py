from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from core.permissions import IsVendor

from .models import Business
from .serializers import BusinessSerializer
from .services.registration import register_business


class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsVendor()]
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsVendor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Business.objects.select_related("owner").all()
        user = self.request.user
        if not user.is_authenticated:
            return qs.filter(status="approved")
        if user.is_staff or getattr(user, "role", None) == "admin":
            return qs
        if getattr(user, "role", None) == "vendor":
            return qs.filter(owner=user)
        return qs.filter(status="approved")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business = register_business(
            owner=request.user,
            name=serializer.validated_data["name"],
            slug=serializer.validated_data["slug"],
        )
        output = self.get_serializer(business)
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)
