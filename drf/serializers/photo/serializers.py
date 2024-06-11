from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.photo.models import Photo

from drf_yasg.utils import swagger_serializer_method


class PhotoSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    voices = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    photo_small = serializers.SerializerMethodField()
    photo_big = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_voices(self, obj):
        return obj.voices.all().count()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_comments(self, obj):
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
