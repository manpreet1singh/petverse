from django.db import transaction
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.models import User

from .models import ProviderProfile, Service
from .serializers import ProviderOwnSerializer, ProviderPublicSerializer, ServiceSerializer


class ProviderBrowseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Public list of verified providers. Filters: ?city=Delhi&category=grooming&home=true"""

    serializer_class = ProviderPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = ProviderProfile.objects.filter(status=ProviderProfile.Status.VERIFIED).prefetch_related("services")
        p = self.request.query_params
        if city := p.get("city"):
            qs = qs.filter(city__iexact=city)
        if category := p.get("category"):
            qs = qs.filter(services__category=category, services__is_active=True)
        if p.get("home") == "true":
            qs = qs.filter(offers_home_service=True)
        return qs.distinct().order_by("-years_experience")


class MyProviderProfileView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    """GET/PATCH your provider profile; POST to register as a provider (starts as pending)."""

    serializer_class = ProviderOwnSerializer

    def get_object(self):
        try:
            return self.request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            raise NotFound("You are not registered as a provider yet")

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, "provider_profile"):
            raise ValidationError("Provider profile already exists")
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        with transaction.atomic():
            s.save(user=request.user)
            request.user.role = User.Role.PROVIDER
            request.user.save(update_fields=["role"])
        return Response(s.data, status=status.HTTP_201_CREATED)


class MyServicesViewSet(viewsets.ModelViewSet):
    """A provider manages the services they offer."""

    serializer_class = ServiceSerializer

    def get_provider(self):
        try:
            return self.request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            raise NotFound("Register as a provider first")

    def get_queryset(self):
        return Service.objects.filter(provider=self.get_provider())

    def perform_create(self, serializer):
        serializer.save(provider=self.get_provider())
