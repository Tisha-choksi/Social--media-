# chat_system/apps.py

from django.apps import AppConfig

class ChatSystemConfig(AppConfig):
    name = 'chat_system'

    def ready(self):
        import chat_system.signals  # This will ensure signals are connected when the app is loaded
