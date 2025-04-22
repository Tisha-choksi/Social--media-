# chat_system/urls.py

from django.urls import path
from .views import (
    StartChatView,
    SendMessageView,
    SendVoiceMessageView,
    AddReactionView,
    DeleteMessageView,
    EditMessageView,
    ListMessagesView
)

urlpatterns = [
    path('start/<str:username>/', StartChatView.as_view(), name='start-chat'),
    # API for sending a message in the chat
    path('send/<str:username>/', SendMessageView.as_view(), name='send-message'),
    # API for sending a voice message in the chat
    path('send-voice-message/', SendVoiceMessageView.as_view(), name='send-voice-message'),

    # API for adding reactions to a message
    path('reaction/', AddReactionView.as_view(), name='add-reaction'),

    # API for deleting a message
    path('delete/<int:message_id>/', DeleteMessageView.as_view(), name='delete-message'),

    # API for editing an existing message
    path('edit/<int:message_id>/', EditMessageView.as_view(), name='edit-message'),

    # API for listing all messages in a chat
    path('list-messages/<int:chat_id>/', ListMessagesView.as_view(), name='list-messages'),
]
