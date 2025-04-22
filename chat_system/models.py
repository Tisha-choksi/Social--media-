from django.db import models
from django.contrib.auth import get_user_model

class Chat(models.Model):
    user_1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_1_chats")
    user_2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_2_chats")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user_1.username} and {self.user_2.username}"
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, default=None)  # Here we allow null and set default
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class Reaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=50)  # Like, Love, Haha, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reacted with {self.reaction_type} to message {self.message.id}"

# Model to store voice messages in chat
class VoiceMessage(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='voice_messages/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voice Message for message {self.message.id}"
