
from rest_framework import status
from rest_framework.response import Response

from base_services.auth_jwt.jwt_helper import AuthJwtTokenService
from base_services.customized.exception import CustomException
from base_services.customized.validation_error import ValidationErr
from users.serializer.user import UserSerializer
from users.services.user import UserService


class UserLoginMixin:

    def response_login(self, id=None, user=None, *args, **kwargs):
        request = kwargs.pop("request", None)
        assert id is not None or user is not None, "Please provide user id or user instance"
        if user is None:
            user = UserService.get_user(id)
            if not user:
                raise CustomException(error=ValidationErr.DOES_NOT_EXIST, params=["User"])
        request.user = user
        return self.create_jwt_login_response(request, **kwargs)

    def create_jwt_login_response(self, request, **kwargs):
        jwt_access_token, rt_instance, jwt_rf_token = AuthJwtTokenService.create_jwt_token(request, **kwargs)
        user_data = UserSerializer(rt_instance.user).data
        user_data.pop("password", None)
        response_data = {
            "user": user_data,
            "jwt_token": jwt_access_token,
            "refresh_token": jwt_rf_token,
        }

        return Response(response_data, status=status.HTTP_200_OK)
