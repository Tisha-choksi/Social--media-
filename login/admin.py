from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP, SocialAccount


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_staff', 'email_verified', 'phone_verified')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'email_verified', 'phone_verified')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'sexuality')
        }),
        ('Preferences', {
            'fields': ('profile_picture', 'theme_color')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'otp', 'created_at', 'expires_at', 'is_used')
    search_fields = ('phone', 'email', 'otp')
    list_filter = ('is_used',)
    readonly_fields = ('created_at', 'expires_at')


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'email', 'created_at')
    search_fields = ('user__username', 'email', 'provider_id')
    list_filter = ('provider',)
    readonly_fields = ('created_at',)
