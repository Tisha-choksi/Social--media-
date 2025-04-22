# chat_system/serializers.py

from rest_framework import serializers
from .models import Chat, Message, Reaction, VoiceMessage
from django.contrib.auth import get_user_model


# Serializer for creating a new chat
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user_1', 'user_2', 'created_at']


# Serializer for creating and displaying messages
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat', 'sender', 'content', 'media_file', 'is_read', 'created_at']


# Serializer for creating reactions to messages
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['message', 'user', 'reaction_type', 'created_at']


# Serializer for sending and storing voice messages
class VoiceMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceMessage
        fields = ['message', 'audio_file', 'created_at']

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'status']
