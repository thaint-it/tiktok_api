from rest_framework import serializers
from posts.models import Post
from posts.models import Like
from posts.models.action import Activity, Favorite
from posts.serializer.post import PostSerializer
from users.serializer.user import UserProfileSerializer


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like


class CreateLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    post_id = serializers.IntegerField(required=False)
    class Meta:
        model = Like
        fields = ["user_id", "post_id"]
        
class CreateFavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    post_id = serializers.IntegerField(required=False)
    class Meta:
        model = Favorite
        fields = ["user_id", "post_id"]
        
class CreateActivitySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    post_id = serializers.IntegerField(required=False)
    action = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    is_read = serializers.BooleanField(required=False)
    class Meta:
        model = Activity
        fields = ["user_id", "post_id","action","content","is_read"]
        
        
class ActivitySerializer(serializers.ModelSerializer):
    user=UserProfileSerializer()
    post=PostSerializer()
    action = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    is_read = serializers.BooleanField(required=False)
    class Meta:
        model = Activity
        fields = '__all__'
    
