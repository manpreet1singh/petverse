from rest_framework import serializers

from .models import User, phone_validator


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])
    code = serializers.RegexField(r"^\d{6}$")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "name", "email", "city", "role", "date_joined"]
        read_only_fields = ["id", "phone", "role", "date_joined"]
