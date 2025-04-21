from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import OTP

User = get_user_model()


# ✅ Automatically verify phone/email when user is created
@receiver(post_save, sender=User)
def update_user_verification(sender, instance, created, **kwargs):
    if created:
        updated = False
        if instance.phone and not instance.phone_verified:
            instance.phone_verified = True
            updated = True
        if instance.email and not instance.email_verified:
            instance.email_verified = True
            updated = True
        if updated:
            instance.save()


# ✅ Clean up expired OTPs when a new OTP is saved
@receiver(post_save, sender=OTP)
def clean_up_expired_otps(sender, instance, **kwargs):
    OTP.objects.filter(
        expires_at__lt=instance.expires_at,
        is_used=False
    ).delete()
