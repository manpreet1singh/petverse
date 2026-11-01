"""Create a few verified demo providers so the browse page has data. Safe to rerun."""

from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.providers.models import ProviderProfile, Service

DEMO = [
    ("+910000000001", "Happy Paws Grooming", "Delhi", True, 6, [
        ("grooming", "Bath & brush", 699, 45), ("grooming", "Full groom + haircut", 1299, 90)]),
    ("+910000000002", "Dr. Mehta's Pet Clinic", "Delhi", True, 12, [
        ("vet_clinic", "General check-up", 500, 30), ("vet_visit", "Home visit consultation", 1200, 45)]),
    ("+910000000003", "Good Boy Academy", "Bengaluru", False, 8, [
        ("training", "Puppy basics (4 sessions)", 3999, 60), ("training", "Behaviour correction", 1500, 60)]),
    ("+910000000004", "Mumbai Dog Walkers", "Mumbai", True, 3, [
        ("walking", "30 min walk", 199, 30), ("boarding", "Daycare (full day)", 799, 600)]),
]


class Command(BaseCommand):
    help = "Seed demo verified providers"

    def handle(self, *args, **opts):
        for phone, name, city, home, yrs, services in DEMO:
            user, _ = User.objects.get_or_create(phone=phone, defaults={"name": name, "role": User.Role.PROVIDER})
            prov, _ = ProviderProfile.objects.update_or_create(
                user=user,
                defaults=dict(business_name=name, city=city, offers_home_service=home,
                              years_experience=yrs, status=ProviderProfile.Status.VERIFIED,
                              bio=f"Trusted pet care in {city}."),
            )
            for cat, sname, price, mins in services:
                Service.objects.update_or_create(
                    provider=prov, name=sname, defaults=dict(category=cat, price_inr=price, duration_minutes=mins))
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(DEMO)} demo providers"))
