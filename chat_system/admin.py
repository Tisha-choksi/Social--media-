# chat_system/admin.py

from django.contrib import admin
from .models import Chat, Message, Reaction, VoiceMessage

# Customizing Chat model in admin
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'created_at')
    search_fields = ('user_1__username', 'user_2__username')
    list_filter = ('created_at',)

admin.site.register(Chat, ChatAdmin)

# chat_system/admin.py

# chat_system/admin.py

from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'updated_at', 'is_read')
    search_fields = ['sender__username', 'receiver__username', 'content']
    list_filter = ['is_read']

admin.site.register(Message, MessageAdmin)


# Customizing Reaction model in admin
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'reaction_type', 'created_at')
    search_fields = ('message__id', 'user__username', 'reaction_type')
    list_filter = ('created_at',)

admin.site.register(Reaction, ReactionAdmin)


# Customizing VoiceMessage model in admin
class VoiceMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'audio_file', 'created_at')
    search_fields = ('message__id',)
    list_filter = ('created_at',)

admin.site.register(VoiceMessage, VoiceMessageAdmin)
