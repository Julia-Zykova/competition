from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.voice.models import Voice


class VoiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Voice
        field = ['photo', 'user']
