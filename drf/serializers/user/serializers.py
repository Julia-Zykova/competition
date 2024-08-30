from rest_framework import serializers

from models_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        depth = 1
        fields = [
            "id",
            "email",
            "get_full_name",
        ]
