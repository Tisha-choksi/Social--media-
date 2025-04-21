from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import random
import requests
import jwt

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP
from .serializers import (
    UserSerializer, LoginSerializer, OTPSerializer,
    OTPVerifySerializer, SignupSerializer,
    SocialAuthSerializer, PasswordResetSerializer,
    PasswordResetConfirmSerializer
)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timedelta(minutes=5)

            if 'phone' in serializer.validated_data:
                print(f"OTP for {serializer.validated_data['phone']}: {otp}")
                OTP.objects.update_or_create(
                    phone=serializer.validated_data['phone'],
                    defaults={'otp': otp, 'expires_at': expires_at, 'is_used': False}
                )
                return Response({'status': 'success', 'message': 'OTP sent to WhatsApp'})

            elif 'email' in serializer.validated_data:
                print(f"OTP for {serializer.validated_data['email']}: {otp}")
                OTP.objects.update_or_create(
                    email=serializer.validated_data['email'],
                    defaults={'otp': otp, 'expires_at': expires_at, 'is_used': False}
                )
                return Response({'status': 'success', 'message': 'OTP sent to email'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            filters = {
                'otp': serializer.validated_data['otp'],
                'is_used': False,
                'expires_at__gt': timezone.now()
            }

            if 'phone' in serializer.validated_data:
                filters['phone'] = serializer.validated_data['phone']
            else:
                filters['email'] = serializer.validated_data['email']

            otp_obj = OTP.objects.filter(**filters).first()

            if otp_obj:
                otp_obj.is_used = True
                otp_obj.save()
                return Response({'status': 'success', 'message': 'OTP verified successfully'})

            return Response({'status': 'error', 'message': 'Invalid or expired OTP'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SocialAuthSerializer, UserSerializer
from .models import User
import requests
import jwt

class SocialLoginView(APIView):
    def post(self, request):
        serializer = SocialAuthSerializer(data=request.data)
        if serializer.is_valid():
            provider = serializer.validated_data['provider']
            token = serializer.validated_data['token']

            try:
                # ✅ GOOGLE LOGIN
                if provider == 'google':
                    if token == "dummy":
                        # Local testing override
                        email = "demouser@gmail.com"
                        first_name = "Demo"
                        last_name = "User"
                    else:
                        user_info = requests.get(
                            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
                        ).json()

                        if 'error' in user_info:
                            return Response(
                                {'status': 'error', 'message': 'Invalid Google token'},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        email = user_info['email']
                        first_name = user_info.get('given_name', '')
                        last_name = user_info.get('family_name', '')

                # ✅ APPLE LOGIN
                elif provider == 'apple':
                    if token == "dummy":
                        email = "appleuser@example.com"
                        first_name = "Apple"
                        last_name = "User"
                    else:
                        decoded = jwt.decode(token, options={"verify_signature": False})
                        email = decoded.get('email')
                        first_name = decoded.get('given_name', '')
                        last_name = decoded.get('family_name', '')

                        if not email:
                            return Response(
                                {'status': 'error', 'message': 'Invalid Apple token'},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                else:
                    return Response(
                        {'status': 'error', 'message': 'Unsupported provider'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # ✅ Create or fetch user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': email.split('@')[0],
                        'first_name': first_name,
                        'last_name': last_name
                    }
                )

                # ✅ Return token & user info
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })

            except Exception as e:
                return Response(
                    {'status': 'error', 'message': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            user = User.objects.filter(
                Q(username=identifier) |
                Q(email=identifier) |
                Q(phone=identifier)
            ).first()

            if user:
                otp = str(random.randint(100000, 999999))
                expires_at = timezone.now() + timedelta(minutes=5)

                if user.phone:
                    OTP.objects.update_or_create(
                        phone=user.phone,
                        defaults={'otp': otp, 'expires_at': expires_at, 'is_used': False}
                    )
                    print(f"OTP for {user.phone}: {otp}")
                    return Response({'status': 'success', 'message': 'OTP sent to WhatsApp'})

                elif user.email:
                    OTP.objects.update_or_create(
                        email=user.email,
                        defaults={'otp': otp, 'expires_at': expires_at, 'is_used': False}
                    )
                    print(f"OTP for {user.email}: {otp}")
                    return Response({'status': 'success', 'message': 'OTP sent to email'})

            return Response({'status': 'error', 'message': 'No account found with this identifier'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']

            otp_obj = OTP.objects.filter(
                otp=otp,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()

            if otp_obj:
                user = None
                if otp_obj.phone:
                    user = User.objects.filter(phone=otp_obj.phone).first()
                elif otp_obj.email:
                    user = User.objects.filter(email=otp_obj.email).first()

                if user:
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    otp_obj.is_used = True
                    otp_obj.save()
                    return Response({'status': 'success', 'message': 'Password reset successfully'})

            return Response({'status': 'error', 'message': 'Invalid or expired OTP'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
