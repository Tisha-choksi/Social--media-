from django.urls import path
from .views import (
    LoginView, SendOTPView, VerifyOTPView,
    SignupView, SocialLoginView,
    PasswordResetView, PasswordResetConfirmView,
    UserDetailsView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('social-login/', SocialLoginView.as_view(), name='social-login'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('me/', UserDetailsView.as_view(), name='user-details'),
]
