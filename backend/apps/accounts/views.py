import logging
import secrets

from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneOTP, User
from .serializers import RequestOTPSerializer, UserSerializer, VerifyOTPSerializer

logger = logging.getLogger(__name__)


class OTPThrottle(AnonRateThrottle):
    rate = "10/hour"


def send_sms(phone, message):
    """Placeholder until an SMS provider (MSG91/Twilio) is wired in."""
    if settings.OTP_DEV_MODE:
        print(f"\n[DEV OTP] {phone}: {message}\n", flush=True)
        return
    raise NotImplementedError("Configure an SMS provider before disabling OTP_DEV_MODE")


class RequestOTPView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        s = RequestOTPSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        phone = s.validated_data["phone"]

        code = f"{secrets.randbelow(10**6):06d}"
        otp = PhoneOTP(phone=phone)
        otp.set_code(code)
        otp.save()
        send_sms(phone, f"Your PetVerse login code is {code}")
        return Response({"detail": "OTP sent"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        s = VerifyOTPSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        phone, code = s.validated_data["phone"], s.validated_data["code"]

        otp = PhoneOTP.objects.filter(phone=phone, used=False).first()
        invalid = Response({"detail": "Invalid or expired code"}, status=400)
        if not otp or otp.is_expired or otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            return invalid
        if not otp.check_code(code):
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            return invalid

        otp.used = True
        otp.save(update_fields=["used"])
        user, created = User.objects.get_or_create(phone=phone)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
                "is_new_user": created,
            }
        )


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
