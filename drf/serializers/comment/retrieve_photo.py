from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'photo', 'user', 'text', 'comments']
