from rest_framework import serializers
from models_app.models.photo.models import Photo
from photo_app.serializers import UserSerializer

class PhotoSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	class Meta:
		model = Photo
		fields = ['id', 'title', 'author', 'image', 'photo_small', 'description', 'comments', 'voices', 'pub_date', 'is_deleted']