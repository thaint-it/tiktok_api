from rest_framework import serializers
from posts.models import Message
from users.serializer.user import UserProfileSerializer


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class CreateMessageSerializer(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField(required=True)
    to_user_id = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=False,allow_null=True)
    content = serializers.CharField(required=True, max_length=500)
   
    class Meta:
        model = Message
        fields = ["from_user_id", "to_user_id", "parent_id", "content"]
        
class ParentMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True, max_length=500)
   
    class Meta:
        model = Message
        fields = ["content"]

class MessageViewSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    content = serializers.CharField()  # Added max_length
    is_read=serializers.BooleanField()
    created_at=serializers.DateTimeField()
    to_user = UserProfileSerializer() 
    from_user= UserProfileSerializer()
    parent=ParentMessageSerializer()

    class Meta:
        model = Message
        fields = [
            "id",
            "content",
            "is_read",
            "created_at",
            "to_user",
            "parent",
            "from_user"
        ]


class MessageCategorySerializer(serializers.ModelSerializer):
    from_user= UserProfileSerializer()
    to_user= UserProfileSerializer()

    class Meta:
        model = Message
        fields = "__all__"
