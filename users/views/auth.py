import os
from django.conf import settings
from django.db import IntegrityError
import jwt
from rest_framework.decorators import action
from rest_framework.authentication import authenticate

from base_services.auth_jwt.jwt_helper import JWTRefreshTokenHelper, AuthJwtTokenService,BaseToken
from base_services.customized.exception import CustomException
from base_services.customized.validation_error import ValidationErr
from base_services.customized.view_mixin import GenericViewMixin

# from constants.common import ErrorMessage
# from constants.status import Statuses
from middlewares.authentication import AuthenticationJWT
from users.mixins import UserLoginMixin
from users.models import User
from users.serializer.user import UpdateAvatarSerializer, UserCreateSerializer, UserSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from users.services.user import UserService
from utils.logging import CommonLogger
from rest_framework import viewsets
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

def generate_uuid_file_name(file_name):
    # Get the file extension (e.g., '.jpg')
    extension = os.path.splitext(file_name)[1]

    # Generate a new UUID
    unique_id = uuid.uuid4()

    # Return the UUID with the original file extension
    return f"{unique_id}{extension}"

class AuthViewSet(viewsets.ViewSet, UserLoginMixin):
    view_set = "auth"
    serializer_class = UserSerializer
    authentication_classes = (AuthenticationJWT,)
    # permission_classes = (SuperAdminPermission,)
    logger = CommonLogger("User")

    @action(detail=False, methods=["POST"], permission_classes=())
    def create_user(self, request):
        try:
            data = request.data.copy()
            print("email",data.get('email'))
            data['user_id']=data.get('email').replace("@gmail.com","")
            data['username']=data.get('email').replace("@gmail.com","")
            serializer = UserCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user= UserService.create_user(request.user, **serializer.validated_data)

            authenticated_user = authenticate(email=user.email, password=data.get('password'))
            kwargs = {
                "id": user.id,
                "request": request,
            }
            return self.response_login(**kwargs)
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return Response({f'error: Invalid data {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=["POST"], authentication_classes=[AuthenticationJWT])
    def update_avatar(self, request, pk=None):
        if 'avatar' in request.FILES:
            user_id = request.POST.get('user_id')
            user = User.objects.filter(id=user_id).first()
            file = request.FILES['avatar']
            folder = 'avatars/'
            # Generate a unique file name using UUID
            unique_file_name = generate_uuid_file_name(file.name)

            # Combine folder and unique file name
            file_name = folder + unique_file_name
            file_name = default_storage.save(file_name, ContentFile(file.read()))
            file_url = os.path.join(settings.MEDIA_URL, file_name)
            user.avatar = file_url
            user.save()
            user_data = UserSerializer(user, many=False).data
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'No file uploaded'}, status=400)


    @action(detail=False, methods=["POST"], permission_classes=())
    def login(self, request):
        """
        @apiVersion 1
        @api {post} /auth/login
        @apiName Login
        @apiGroup Auth

        @apiSuccess 200
        """
        data = request.data.copy()
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(Q(email=data.get('email')) | Q(user_id=data.get('user_id'))).first()
            if not user:
                raise CustomException(error=ValidationErr.DOES_NOT_EXIST, params=["user"])
            user = authenticate(username=user.username, password=data.get('password'))
            if not user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            kwargs = {
                "id": user.id,
                "request": request,
            }
            return self.response_login(**kwargs)

    @action(detail=False, methods=["POST"], permission_classes=())
    def refresh_jwt_token(self, request):
        """
        @apiVersion 1
        @api {post} /auth/refresh_jwt_token Refresh jwt token
        @apiName RefreshJwtToken
        @apiGroup Auth

        @apiParam {String} refresh_token The refresh token is used to obtain a new token

        @apiSuccess 200
        """
        data = request.data.copy()
        jwt_refresh_token = data.get("refresh_token", None)
        if not jwt_refresh_token:
            raise CustomException(error=ValidationErr.REQUIRED, params=["refresh_token"])
        payload = JWTRefreshTokenHelper.decrypt(jwt_refresh_token)
        if not AuthJwtTokenService.validate_refresh_token(request, payload.get('uuid_token')):
            raise CustomException(error=ValidationErr.INVALID, params=["refresh_token"])

        return self.response_login(user=request.user, request=request)

    # @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    # def get_users(self, request):
    #     page = request.query_params.get('page') or 1
    #     per_page = request.query_params.get('per_page') or 10
    #     users, total = UserService.get_users(
    #         page=page,
    #         filter_by_role=request.query_params.get('filter_by_role'),
    #         filter_by_status=request.query_params.get('filter_by_status'),
    #         search=request.query_params.get('search')
    #     )
    #     data = dict(
    #         result=users,
    #         total=total
    #     )
    #     return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def get_user(self, request):
        auth = get_authorization_header(request).split()
        token = auth[1]
        payload = jwt.decode(token, settings.JWT_AUTH.get('JWT_PUBLIC_KEY'), algorithms="RS256")
        user = User.objects.get(id=payload['id'])
        if not user:
            raise CustomException(error=ValidationErr.DOES_NOT_EXIST, params=["user"])
        user_data = UserSerializer(user, many=False).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], authentication_classes=[AuthenticationJWT])
    def get_user_by_id(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise CustomException(error=ValidationErr.DOES_NOT_EXIST, params=["user"])
        user_data = UserSerializer(user, many=False).data
        return Response(user_data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=["POST"], authentication_classes=[], permission_classes=[])
    # def reset_password(self, request, pk=None):
    #     user = User.objects.filter(email=request.data.get('email')).first()
    #     if not user:
    #         raise CustomException(error=ValidationErr.DOES_NOT_EXIST, params=["user"])
    #     UserService.reset_password(user)
    #     return Response(status=status.HTTP_200_OK)
