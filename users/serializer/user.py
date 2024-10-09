from rest_framework import serializers
from users.models import User
from users.models.user import Follower, FolowerActivity


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    tiktok_id = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    tiktok_id = serializers.CharField(required=False, max_length=255)
    username = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(required=False, max_length=255)


class UserAvatarSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=255)
    avatar = serializers.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = ["user_id", "avatar"]


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    tiktok_id = serializers.CharField()
    avatar = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "tiktok_id", "username", "avatar", "first_name"]


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserProfileSerializer()
    following = UserProfileSerializer()

    class Meta:

        model = Follower
        fields = "__all__"


class FollowerActivitySerializer(serializers.ModelSerializer):
    follower = UserProfileSerializer()
    following = UserProfileSerializer()
    is_read = serializers.BooleanField()
    class Meta:
        model = FolowerActivity
        fields = "__all__"
