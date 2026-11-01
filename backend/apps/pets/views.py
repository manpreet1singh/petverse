from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Pet
from .serializers import PetSerializer, VaccinationSerializer


class PetViewSet(viewsets.ModelViewSet):
    """CRUD for the logged-in owner's pets. Owners never see other people's pets."""

    serializer_class = PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user).prefetch_related("vaccinations")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VaccinationViewSet(viewsets.ModelViewSet):
    """Vaccinations nested under /pets/<pet_pk>/vaccinations/."""

    serializer_class = VaccinationSerializer

    def get_pet(self):
        return get_object_or_404(Pet, pk=self.kwargs["pet_pk"], owner=self.request.user)

    def get_queryset(self):
        return self.get_pet().vaccinations.all()

    def perform_create(self, serializer):
        serializer.save(pet=self.get_pet())
