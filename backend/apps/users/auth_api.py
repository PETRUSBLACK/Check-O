from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from .models import User, UserRole
from .serializers import UserSerializer


class VendorBusinessPayloadSerializer(serializers.Serializer):
    """Optional: create draft business profile during vendor registration."""

    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    legal_name = serializers.CharField(max_length=255)
    registration_number = serializers.CharField(max_length=128)
    tax_identifier = serializers.CharField(
        max_length=64, required=False, allow_blank=True, default=""
    )
    business_phone = serializers.CharField(
        max_length=32, required=False, allow_blank=True, default=""
    )
    address = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(
        choices=[UserRole.CUSTOMER, UserRole.VENDOR],
        required=False,
        default=UserRole.CUSTOMER,
    )
    vendor_business = VendorBusinessPayloadSerializer(
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "vendor_business",
        )

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        role = attrs.get("role", UserRole.CUSTOMER)
        vb = attrs.get("vendor_business")
        if vb and role != UserRole.VENDOR:
            raise serializers.ValidationError(
                {"vendor_business": "Only vendors can submit business details at signup."}
            )
        return attrs

    def create(self, validated_data):
        from apps.businesses.services.registration import register_business

        vendor_payload = validated_data.pop("vendor_business", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        if user.role == UserRole.VENDOR and vendor_payload:
            register_business(
                owner=user,
                name=vendor_payload["name"],
                slug=vendor_payload["slug"],
                legal_name=vendor_payload["legal_name"],
                registration_number=vendor_payload["registration_number"],
                tax_identifier=vendor_payload.get("tax_identifier") or "",
                business_phone=vendor_payload.get("business_phone") or "",
                address=vendor_payload["address"],
            )
        return user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: UserSerializer},
        tags=["auth"],
        summary="Register customer or vendor account",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        tags=["auth"],
        summary="Get current authenticated user",
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)
