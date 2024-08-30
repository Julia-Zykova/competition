from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.comment.models import Comment


class CommentRetrieveSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    @staticmethod
    def get_comments(obj):
        return CommentRetrieveSerializer(obj.comments.all().order_by("-created_at")[:5], many=True).data

    class Meta:
        model = Comment
        fields = ["id", "created_at", "photo", "user", "text", "comments"]
