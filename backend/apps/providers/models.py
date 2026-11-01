from django.conf import settings
from django.db import models


class ServiceCategory(models.TextChoices):
    GROOMING = "grooming", "Grooming"
    VET_VISIT = "vet_visit", "Vet home visit"
    VET_CLINIC = "vet_clinic", "Vet clinic"
    TRAINING = "training", "Training"
    WALKING = "walking", "Walking"
    BOARDING = "boarding", "Boarding & daycare"


class ProviderProfile(models.Model):
    """A business or individual offering pet services. Admins verify before they go live."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending verification"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provider_profile"
    )
    business_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=80, db_index=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    offers_home_service = models.BooleanField(default=False)
    years_experience = models.PositiveSmallIntegerField(default=0)
    license_number = models.CharField(max_length=80, blank=True, help_text="Required for vets")
    logo = models.ImageField(upload_to="providers/", null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    commission_percent = models.DecimalField(max_digits=4, decimal_places=2, default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class Service(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="services")
    category = models.CharField(max_length=16, choices=ServiceCategory.choices, db_index=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price_inr = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    species = models.CharField(max_length=60, blank=True, help_text="e.g. dog,cat — blank means all")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "price_inr"]

    def __str__(self):
        return f"{self.name} – {self.provider}"
