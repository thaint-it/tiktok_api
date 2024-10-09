from rest_framework.decorators import action


# from constants.common import ErrorMessage
# from constants.status import Statuses
from middlewares.authentication import AuthenticationJWT
from posts.models import Message
from posts.serializer.message import (
    MessageCategorySerializer,
    MessageSerializer,
    CreateMessageSerializer,
    MessageViewSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator

from utils.logging import CommonLogger
from rest_framework import viewsets
from django.db.models import Q,Subquery,OuterRef,Max,Case,When,IntegerField,F


class MessageViewSet(viewsets.ViewSet):
    view_set = "messages"
    serializer_class = MessageSerializer
    auth_jwt = AuthenticationJWT()
    authentication_classes = (AuthenticationJWT,)
    logger = CommonLogger("Messages")

    def list(self, request):
        try:
            auth_jwt = AuthenticationJWT()
            user = auth_jwt.authenticate(request)
            page_number = request.query_params.get("page") or 1
            per_page = request.query_params.get("per_page") or 20
            sender_id = user[0].id
            receiver_id = request.query_params.get("receiver_id")

            # Fetch posts with related user data
            messages = (
                Message.objects.filter(from_user_id=sender_id, to_user_id=receiver_id)
                | Message.objects.filter(to_user_id=sender_id, from_user_id=receiver_id)
            ).order_by("created_at")
            paginator = Paginator(messages, per_page)
            page_obj = paginator.page(page_number)
            serializer = MessageViewSerializer(page_obj.object_list, many=True)
            response_data = {
                "messages": serializer.data,
                "total_pages": paginator.num_pages,
                "current_page": page_number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def get_by_id(self, request):
        try:
            id = request.query_params.get("id")
            message = Message.objects.filter(id=id).first()
            serializer = MessageViewSerializer(message, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data.copy()
        auth_jwt = AuthenticationJWT()
        user = auth_jwt.authenticate(request)

        # Save the video file
        # Create data dictionary for the serializer
        data["from_user_id"] = user[0].id
        # Instantiate the serializer with data
        serializer = CreateMessageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"status": "error", "message": "No file uploaded"}, status=400)

    @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def message_categories(self, request):
        try:
            auth_jwt = AuthenticationJWT()
            user = auth_jwt.authenticate(request)
            current_user_id = user[0].id
            current_user = user[0]
            
            last_messages = (
            Message.objects.filter(
                Q(from_user=current_user) | Q(to_user=current_user)
            )
            .annotate(
                # Normalize user pairs to create a unique conversation identifier
                conversation_id=Case(
                    When(from_user=current_user, then=F('to_user')),
                    When(to_user=current_user, then=F('from_user')),
                output_field=IntegerField(),
            )
            )
            .values('conversation_id')  # Group by the normalized conversation ID
            .annotate(
                last_message_id=Max('id')  # Get the ID of the last message for each conversation
            )
            )

            # Extract the last message IDs
            last_ids = [item['last_message_id'] for item in last_messages]
            # Fetch the last messages based on the IDs
            last_messages_queryset = Message.objects.filter(id__in=last_ids)

            # Ensure that we return only the last message per conversation
            unique_last_messages = last_messages_queryset.distinct().order_by("-created_at")
            serializer=MessageCategorySerializer(unique_last_messages,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
