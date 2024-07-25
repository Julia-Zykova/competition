from rest_framework import serializers

from drf.serializers import CommentRetrieveSerializer, UserSerializer
from models_app.models.comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = UserSerializer()

    @staticmethod
    def get_comments(obj):
        return CommentRetrieveSerializer(obj.comments.order_by("-created_at")[:3], many=True).data

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'photo', 'user', 'text', 'comments']
