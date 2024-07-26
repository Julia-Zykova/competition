from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.photo.models import Photo

from drf_yasg.utils import swagger_serializer_method


class PhotoBaseSerializer(serializers.ModelSerializer):
    voices = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    photo_small = serializers.SerializerMethodField()
    photo_big = serializers.SerializerMethodField()

    @staticmethod
    def get_voices(obj) -> int:
        return obj.sum_voices

    @staticmethod
    def get_comments(obj) -> int:
        return obj.sum_comments

    @staticmethod
    def get_photo_small(obj) -> str:
        return obj.photo_small.url

    @staticmethod
    def get_photo_big(obj) -> str:
        return obj.photo_big.url

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'image', 'photo_small', 'photo_big', 'description',
            'comments', 'voices', 'pub_date', 'state'
        ]
        read_only_fields = ['pub_date', 'id', 'state']


class PhotoSerializer(PhotoBaseSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'author', 'image', 'photo_small', 'photo_big', 'description',
            'comments', 'voices', 'pub_date', 'state'
        ]
        read_only_fields = ['author', 'pub_date', 'id', 'state']
