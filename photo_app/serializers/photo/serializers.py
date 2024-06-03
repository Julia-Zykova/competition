from rest_framework import serializers

from drf.serializers import ShortInfUserSerializer
from models_app.models.photo.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    author = ShortInfUserSerializer()
    voices = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    photo_small = serializers.SerializerMethodField()
    photo_big = serializers.SerializerMethodField()

    def get_voices(self, obj):
        return obj.voices.all().count()

    def get_comments(self, obj):
        return obj.comments.all().count()

    def get_photo_small(self, obj):
        return obj.photo_small.url

    def get_photo_big(self, obj):
        return obj.photo_big.url

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'author', 'image', 'photo_small', 'photo_big', 'description',
            'comments', 'voice', 'pub_date', 'is_deleted', 'state'
        ]