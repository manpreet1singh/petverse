from rest_framework import serializers

from .models import Pet, Vaccination


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ["id", "vaccine_name", "date_given", "next_due", "administered_by", "notes"]


class PetSerializer(serializers.ModelSerializer):
    age_months = serializers.IntegerField(read_only=True)
    vaccinations = VaccinationSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id", "name", "species", "breed", "gender", "date_of_birth", "age_months",
            "weight_kg", "is_neutered", "photo", "allergies", "medical_notes",
            "vaccinations", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
