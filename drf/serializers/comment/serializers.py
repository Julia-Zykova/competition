from rest_framework import serializers
from models_app.models.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'photo', 'user', 'text', 'comment']
