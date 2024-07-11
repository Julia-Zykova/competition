from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models import Photo
from models_app.models.voice.models import Voice


class VoiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photo = serializers.SerializerMethodField()

    @staticmethod
    def get_photo(obj):
        photo = Photo.objects.get(id=obj.photo.id)
        return f"title -'{photo.title}', author - '{photo.author.email}'"

    class Meta:
        model = Voice
        fields = ['photo', 'user', 'id', 'is_deleted']
