from django.apps import AppConfig


class VoicetextConfig(AppConfig):
    name = 'voicetext'

    def ready(self):
        import voicetext.signals
