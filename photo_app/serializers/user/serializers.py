from rest_framework import serializers
from models_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		depth = 1
		fields = ['first_name', 'last_name', 'email']