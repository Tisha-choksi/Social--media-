# chat_system/views.py

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chat, Message, Reaction, VoiceMessage
from .serializers import ChatSerializer, MessageSerializer, ReactionSerializer, VoiceMessageSerializer
from django.contrib.auth import get_user_model


class StartChatView(APIView):
    def post(self, request, username):
        try:
            user_to = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is not starting a chat with themselves
        if request.user == user_to:
            return Response({'error': 'You cannot start a chat with yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the chat between the users
        chat = Chat.objects.create(user_1=request.user, user_2=user_to)
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from django.contrib.auth import get_user_model

class SendMessageView(APIView):
    def post(self, request, username):
        # Ensure the target user exists
        try:
            user_to_chat = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')

        if not content:
            return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the message object with sender and receiver
        message = Message.objects.create(
            sender=request.user,
            receiver=user_to_chat,
            content=content
        )

        return Response({'message': 'Message sent successfully!'}, status=status.HTTP_201_CREATED)

class SendVoiceMessageView(APIView):
    def post(self, request):
        chat_id = request.data.get('chat_id')
        audio_file = request.data.get('audio_file', None)

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a voice message
        message = Message.objects.create(chat=chat, sender=request.user)
        voice_message = VoiceMessage.objects.create(message=message, audio_file=audio_file)
        serializer = VoiceMessageSerializer(voice_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddReactionView(APIView):
    def post(self, request):
        message_id = request.data.get('message_id')
        reaction_type = request.data.get('reaction_type')

        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        # Add reaction
        reaction = Reaction.objects.create(message=message, user=request.user, reaction_type=reaction_type)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteMessageView(APIView):
    def delete(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, sender=request.user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found or not authorized to delete.'},
                            status=status.HTTP_404_NOT_FOUND)

        message.delete()
        return Response({'message': 'Message deleted successfully.'}, status=status.HTTP_200_OK)


class EditMessageView(APIView):
    def post(self, request, message_id):
        new_content = request.data.get('content')
        try:
            message = Message.objects.get(id=message_id, sender=request.user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found or not authorized to edit.'}, status=status.HTTP_404_NOT_FOUND)

        message.content = new_content
        message.save()
        return Response({'message': 'Message updated successfully.'}, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message, Chat
from .serializers import MessageSerializer

class ListMessagesView(APIView):
    """
    List all messages for a specific chat.
    """
    def get(self, request, chat_id):
        # Check if the chat exists
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all messages for this chat
        messages = Message.objects.filter(chat=chat)

        # Serialize the messages
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
