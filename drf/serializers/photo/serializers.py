from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.photo.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    #author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = UserSerializer()
    voices = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    photo_small = serializers.SerializerMethodField()
    photo_big = serializers.SerializerMethodField()

    @staticmethod
    def get_voices(obj):
        return obj.voices.all().count()

    @staticmethod
    def get_comments(obj):
        return obj.comments.all().count()

    @staticmethod
    def get_photo_small(obj):
        return obj.photo_small.url

    @staticmethod
    def get_photo_big(obj):
        return obj.photo_big.url

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'author', 'image', 'photo_small', 'photo_big', 'description',
            'comments', 'voices', 'pub_date', 'state'
        ]
        read_only_fields = ['author', 'pub_date', 'id', 'state']
