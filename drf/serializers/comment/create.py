from rest_framework import serializers

from drf.serializers import UserSerializer
from models_app.models.comment.models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
