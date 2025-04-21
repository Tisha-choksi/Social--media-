from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP, SocialAccount
import re
from django.db.models import Q



# 🔹 Serializer to return user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'dob', 'gender', 'sexuality', 'profile_picture',
            'theme_color', 'email_verified', 'phone_verified'
        ]


# 🔹 Login with username/email/phone
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        user = None
        if re.match(r'^\d{10}$', identifier):
            user = User.objects.filter(phone=identifier).first()
        elif '@' in identifier:
            user = User.objects.filter(email=identifier).first()
        else:
            user = User.objects.filter(username=identifier).first()

        if user:
            user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# 🔹 Send OTP serializer
class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if not data.get('phone') and not data.get('email'):
            raise serializers.ValidationError("Either phone or email is required.")
        return data


# 🔹 Verify OTP serializer
class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        if not data.get('phone') and not data.get('email'):
            raise serializers.ValidationError("Either phone or email is required.")
        return data


# 🔹 Signup with password validation
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$',
            message="Password must contain at least 8 characters, one uppercase, one lowercase, one number, and one special character"
        )]
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'password', 'confirm_password',
            'first_name', 'last_name', 'dob', 'gender', 'sexuality'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


# 🔹 Social login (Google/Apple) via token
class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'apple'])
    token = serializers.CharField()


# 🔹 Start password reset
class PasswordResetSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate(self, data):
        identifier = data.get('identifier')

        # ✅ Check if user exists using Q (not serializers.Q!)
        if not User.objects.filter(
            Q(username=identifier) |
            Q(email=identifier) |
            Q(phone=identifier)
        ).exists():
            raise serializers.ValidationError("No account found with this identifier")

        return data

# 🔹 Confirm password reset
class PasswordResetConfirmSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        # Password policy validation
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', data['new_password']):
            raise serializers.ValidationError(
                "Password must contain at least 8 characters, one uppercase, one lowercase, one number, and one special character."
            )

        return data
