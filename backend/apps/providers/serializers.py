from rest_framework import serializers

from .models import ProviderProfile, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id", "category", "name", "description", "price_inr",
            "duration_minutes", "species", "is_active",
        ]


class ProviderPublicSerializer(serializers.ModelSerializer):
    """What pet owners see when browsing."""

    services = serializers.SerializerMethodField()

    class Meta:
        model = ProviderProfile
        fields = [
            "id", "business_name", "bio", "city", "offers_home_service",
            "years_experience", "logo", "services",
        ]

    def get_services(self, obj):
        return ServiceSerializer(obj.services.filter(is_active=True), many=True).data


class ProviderOwnSerializer(serializers.ModelSerializer):
    """What a provider sees and edits on their own profile."""

    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ProviderProfile
        fields = [
            "id", "business_name", "bio", "city", "address", "pincode",
            "offers_home_service", "years_experience", "license_number", "logo",
            "status", "commission_percent", "services", "created_at",
        ]
        read_only_fields = ["id", "status", "commission_percent", "created_at"]
