from datetime import date

from django.conf import settings
from django.db import models


class Pet(models.Model):
    class Species(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        BIRD = "bird", "Bird"
        RABBIT = "rabbit", "Rabbit"
        FISH = "fish", "Fish"
        OTHER = "other", "Other"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNKNOWN = "unknown", "Unknown"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=80)
    species = models.CharField(max_length=16, choices=Species.choices)
    breed = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=8, choices=Gender.choices, default=Gender.UNKNOWN)
    date_of_birth = models.DateField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_neutered = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="pets/", null=True, blank=True)
    allergies = models.TextField(blank=True)
    medical_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"

    @property
    def age_months(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        dob = self.date_of_birth
        return (today.year - dob.year) * 12 + today.month - dob.month - (today.day < dob.day)


class Vaccination(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine_name = models.CharField(max_length=120)
    date_given = models.DateField()
    next_due = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.vaccine_name} for {self.pet.name}"
