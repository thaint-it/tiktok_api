from rest_framework import serializers
from posts.models import Post
from users.serializer.user import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields='__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=255)
    title = serializers.CharField(required=False, max_length=500)
    description = serializers.CharField(required=False, max_length=500)
    thumbnail = serializers.CharField(required=False, max_length=250)
    isPrivate = serializers.BooleanField(default=False)
    url = serializers.CharField(required=False, max_length=250)

    class Meta:
        model = Post
        fields = ["user_id", "title", "description", "url", "thumbnail", "isPrivate"]


class PostViewSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.CharField()
    isPrivate = serializers.BooleanField()
    url = serializers.CharField()
    view_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    share_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    user = UserProfileSerializer()  #

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "description",
            "url",
            "thumbnail",
            "isPrivate",
            "view_count",
            "comment_count",
            "like_count",
            "favorite_count",
            "share_count",
        ]
