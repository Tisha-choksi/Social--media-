# chat_system/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, Reaction, Chat
from django.utils import timezone

# Signal to update message timestamps or perform actions after a message is saved
@receiver(post_save, sender=Message)
def update_message_timestamp(sender, instance, created, **kwargs):
    # If a new message is created, update the timestamp
    if created:
        instance.created_at = timezone.now()
        instance.save()

# Signal to update chat after a new message is added (optional)
@receiver(post_save, sender=Message)
def update_chat_last_message(sender, instance, created, **kwargs):
    if created:
        # If this is the first message, set the chat to have a last message
        chat = instance.chat
        chat.updated_at = timezone.now()  # Update chat's updated_at timestamp
        chat.save()

# Signal to delete all reactions when a message is deleted
@receiver(post_delete, sender=Message)
def delete_reactions_on_message_delete(sender, instance, **kwargs):
    # Delete all reactions related to this message
    instance.reactions.all().delete()

# Signal to update the "last_activity" field or similar after a user blocks someone
@receiver(post_save, sender=Chat)
def update_chat_activity(sender, instance, **kwargs):
    # You can implement logic to track when the last message or activity happens in the chat
    # Example: If a user sends a message, update 'last_activity' in Chat model
    pass
