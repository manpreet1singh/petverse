from unittest.mock import patch

from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.pets.models import Pet
from apps.providers.models import ProviderProfile

PHONE = "+919876543210"


class AuthFlowTests(APITestCase):
    def setUp(self):
        cache.clear()  # reset OTP rate limits between tests

    def login(self, phone=PHONE):
        with patch("apps.accounts.views.secrets.randbelow", return_value=123456):
            r = self.client.post("/api/auth/otp/request/", {"phone": phone})
        self.assertEqual(r.status_code, 200)
        r = self.client.post("/api/auth/otp/verify/", {"phone": phone, "code": "123456"})
        self.assertEqual(r.status_code, 200, r.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {r.data['access']}")
        return r.data

    def test_otp_login_creates_user(self):
        data = self.login()
        self.assertTrue(data["is_new_user"])
        self.assertTrue(User.objects.filter(phone=PHONE).exists())
        self.assertEqual(self.client.get("/api/auth/me/").data["phone"], PHONE)

    def test_wrong_code_rejected_and_code_single_use(self):
        with patch("apps.accounts.views.secrets.randbelow", return_value=111111):
            self.client.post("/api/auth/otp/request/", {"phone": PHONE})
        r = self.client.post("/api/auth/otp/verify/", {"phone": PHONE, "code": "000000"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.client.post("/api/auth/otp/verify/", {"phone": PHONE, "code": "111111"}).status_code, 200)
        self.assertEqual(self.client.post("/api/auth/otp/verify/", {"phone": PHONE, "code": "111111"}).status_code, 400)

    def test_requires_auth(self):
        self.assertEqual(self.client.get("/api/pets/").status_code, 401)

    def test_pet_crud_and_isolation(self):
        self.login()
        r = self.client.post("/api/pets/", {"name": "Bruno", "species": "dog", "breed": "Labrador", "date_of_birth": "2023-01-15"})
        self.assertEqual(r.status_code, 201, r.data)
        pet_id = r.data["id"]
        r = self.client.post(f"/api/pets/{pet_id}/vaccinations/", {"vaccine_name": "Rabies", "date_given": "2025-01-10"})
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(len(self.client.get(f"/api/pets/{pet_id}/").data["vaccinations"]), 1)

        # another owner can't see or touch Bruno
        self.client.credentials()
        self.login("+919999999999")
        self.assertEqual(self.client.get("/api/pets/").data["count"], 0)
        self.assertEqual(self.client.get(f"/api/pets/{pet_id}/").status_code, 404)
        self.assertEqual(self.client.get(f"/api/pets/{pet_id}/vaccinations/").status_code, 404)
        self.assertTrue(Pet.objects.filter(pk=pet_id).exists())

    def test_provider_signup_and_browse(self):
        self.login()
        r = self.client.post("/api/provider/profile/", {"business_name": "Happy Paws", "city": "Delhi", "offers_home_service": True})
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(r.data["status"], "pending")
        self.assertEqual(User.objects.get(phone=PHONE).role, "provider")
        r = self.client.post("/api/provider/services/", {"category": "grooming", "name": "Full groom", "price_inr": "1200"})
        self.assertEqual(r.status_code, 201, r.data)

        self.client.credentials()
        self.assertEqual(self.client.get("/api/providers/?city=delhi").data["count"], 0)  # pending = hidden
        ProviderProfile.objects.update(status="verified")
        self.assertEqual(self.client.get("/api/providers/?city=delhi&category=grooming").data["count"], 1)
        self.assertEqual(self.client.get("/api/providers/?category=walking").data["count"], 0)
