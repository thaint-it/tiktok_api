import os
from django.conf import settings
from rest_framework.decorators import action


# from constants.common import ErrorMessage
# from constants.status import Statuses
from middlewares.authentication import AuthenticationJWT
from posts.models.action import Activity
from posts.models.post import Post
from posts.serializer.post import CreatePostSerializer, PostViewSerializer
from posts.serializer.action import ActivitySerializer, CreateFavoriteSerializer, CreateLikeSerializer,CreateActivitySerializer
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator

from users.services.user import UserService
from utils.logging import CommonLogger
from rest_framework import viewsets
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from users.models import User
from rest_framework.permissions import AllowAny
from django.db.models import Q


def generate_uuid_file_name(file_name):
    # Get the file extension (e.g., '.jpg')
    extension = os.path.splitext(file_name)[1]

    # Generate a new UUID
    unique_id = uuid.uuid4()

    # Return the UUID with the original file extension
    return f"{unique_id}{extension}"


class PostViewSet(viewsets.ViewSet):
    view_set = "post"
    serializer_class = CreatePostSerializer
    authentication_classes = (AuthenticationJWT,)
    logger = CommonLogger("Post")

    @action(detail=False, methods=["GET"], permission_classes=())
    def list_post(self, request):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)
        try:
            page_number = request.query_params.get("page") or 1
            per_page = request.query_params.get("per_page") or 1
            
            # Fetch posts with related user data
            posts = Post.objects.select_related("user").order_by('-created_at').all()
            paginator = Paginator(posts, per_page)
            page_obj = paginator.page(page_number)
            
            # post_list = list(page_obj.object_list.values())
            serializer = PostViewSerializer(page_obj.object_list, many=True)
            for post in serializer.data:
                post["view_count"] = 11
                post["like_count"] = 122
                post["favorite_count"] = 55
                post["comment_count"] = 99
                post["share_count"] = 33

            response_data = {
                "posts": serializer.data,
                "total_pages": paginator.num_pages,
                "current_page": page_number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }


            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["POST"], authentication_classes=[AuthenticationJWT])
    def create_post(self, request):
        if "video" in request.FILES and "thumbnail" in request.FILES:
            # Get user ID
            user_id = request.POST.get("user_id")
            user = User.objects.filter(id=user_id).first()

            # Prepare the file URLs
            video_file = request.FILES["video"]
            thumbnail_file = request.FILES["thumbnail"]

            # Save the video file
            video_folder = "posts/"
            unique_video_file_name = generate_uuid_file_name(video_file.name)
            video_file_name = video_folder + unique_video_file_name
            default_storage.save(video_file_name, ContentFile(video_file.read()))
            video_file_url = os.path.join(settings.MEDIA_URL, video_file_name)
            # Save the thumbnail file
            thumbnail_folder = "thumbnails/"
            unique_thumbnail_file_name = generate_uuid_file_name(thumbnail_file.name)
            thumbnail_file_name = thumbnail_folder + unique_thumbnail_file_name
            default_storage.save(
                thumbnail_file_name, ContentFile(thumbnail_file.read())
            )
            thumbnail_file_url = os.path.join(settings.MEDIA_URL, thumbnail_file_name)

            # Create data dictionary for the serializer
            data = {
                "user_id": user_id,  # Set user object directly or use user_id if you want to pass the ID
                "title": request.POST.get("title"),
                "description": request.POST.get("description"),
                "thumbnail": thumbnail_file_url,  # Assign the correct thumbnail URL
                "isPrivate": request.POST.get(
                    "isPrivate", False
                ),  # Handle isPrivate field
                "url": video_file_url,
            }

            # Instantiate the serializer with data
            serializer = CreatePostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"status": "error", "message": "No file uploaded"}, status=400)
    
    @action(detail=False, methods=["POST"], authentication_classes=[AuthenticationJWT])
    def like_post(self, request):
        data = request.data.copy()
        auth_jwt = AuthenticationJWT()
        user = auth_jwt.authenticate(request)
        # Save the video file
        # Create data dictionary for the serializer
        data["user_id"] = user[0].id
    
        # Instantiate the serializer with data
        serializer = CreateLikeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            like_data={
                "user_id":data["user_id"],
                "post_id":data["post_id"],
                "action":"LIKE"
            }
            activity_serializer = CreateActivitySerializer(data=like_data)
            if activity_serializer.is_valid(raise_exception=True):
                activity_serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "No file uploaded"}, status=400)
    
    @action(detail=False, methods=["POST"], authentication_classes=[AuthenticationJWT])
    def favorite_post(self, request):
        data = request.data.copy()
        auth_jwt = AuthenticationJWT()
        user = auth_jwt.authenticate(request)
        # Save the video file
        # Create data dictionary for the serializer
        data["user_id"] = user[0].id
    
        # Instantiate the serializer with data
        serializer = CreateFavoriteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            favorite_data={
                "user_id":data["user_id"],
                "post_id":data["post_id"],
                "action":"FAVORITE"
            }
            # activity_serializer = CreateActivitySerializer(data=like_data)
            # if activity_serializer.is_valid(raise_exception=True):
            #     activity_serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "No file uploaded"}, status=400)
    
    @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def activity_categories(self, request):
        try:
            auth_jwt = AuthenticationJWT()
            user = auth_jwt.authenticate(request)
            current_user_id = user[0].id
            
            last_activity = Activity.objects.filter(
                post__user_id=current_user_id
            ).order_by('-created_at').first()
            
            serializer=ActivitySerializer(last_activity)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def activities(self, request):
        try:
            auth_jwt = AuthenticationJWT()
            user = auth_jwt.authenticate(request)
            current_user_id = user[0].id
            
            last_activity = Activity.objects.filter(
                post__user_id=current_user_id
            ).order_by('-created_at').all()
            
            serializer=ActivitySerializer(last_activity,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

