from rest_framework import serializers
from django.db.models import Count
from models_app.models.photo.models import Photo
from photo_app.serializers import UserSerializer

class PhotoSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    photo_small = serializers.SerializerMethodField()
    voices = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_photo_small(self, obj):
        path = obj.photo_small.path.split("mnt/d/competition")
        new_path = path[1]
        return new_path

    def get_voices(self, obj):
        sum_voices = len(obj.voices.values())
        return sum_voices

    def get_comments(self, obj):
        sum_comments = len(obj.comments.values())
        return sum_comments

    class Meta:
        model = Photo
        fields = ['id', 'title', 'author', 'image', 'photo_small', 'description', 'comments', 'voices', 'pub_date', 'is_deleted']

        