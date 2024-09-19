from cProfile import Profile
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    user_id = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    user_id = serializers.CharField(required=False, max_length=255)
    username = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(required=False, max_length=255)
   


class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']