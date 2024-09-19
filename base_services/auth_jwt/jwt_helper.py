
import datetime
from typing import Tuple
from django.conf import settings
from rest_framework import status
import jwt
from base_services.customized.exception import CustomException
from base_services.customized.validation_error import ValidationErr
from users.models import AuthRefreshToken
from users.services.auth_refresh_token import AuthRefreshTokenService
from users.services.user import UserService
from utils.utils import Utils
import time


_BYTE_ENCODING = "ASCII"


class BaseToken:
    @staticmethod
    def _get_headers():
        return {
            "alg": "RS256",
            "typ": "JWT",
        }

    @staticmethod
    def _bytes_decode(token):
        return token.decode(_BYTE_ENCODING)

    @staticmethod
    def _bytes_encode(token):
        return token.encode(_BYTE_ENCODING)

    @staticmethod
    def _get_secret_key():
        return settings.JWT_AUTH.get('JWT_PRIVATE_KEY')
        

    def encode(self, payload):
        token = jwt.encode(payload, self._get_secret_key(), algorithm='RS256')
        return token

    def decode(self, token, bytes_decoded=True):
        token = self._bytes_encode(token) if bytes_decoded else token
        try:
            payload = jwt.decode(token, self._get_secret_key(), headers=self._get_headers())
        except Exception:
            payload = None
        return payload



class ChromeExtensionJWTToken(BaseToken):
    JWT_EXP_DAYS = 2

    def encode_token(self, id: int, email: str, username: str, user_id:str):
        payload = {
            "id": id,
            "email": email,
            "username": username,
            "user_id": user_id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=self.JWT_EXP_DAYS),
        }
        token = self.encode(payload)
        return token


class JWTRefreshTokenHelper:
    JWT_ALGORITHM = "RS256"
    JWT_EXP_DAYS = 7

    @classmethod
    def encrypt(cls, uuid_token: str, user_id: int, email: str) -> str:
        """
        To encrypt refresh_token to jwt token
        """
        try:
            exp_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=cls.JWT_EXP_DAYS)
            payload = dict(
                user_id=user_id,
                email=email, uuid_token=uuid_token, exp=exp_time
            )
            # headers = {"alg": cls.JWT_ALGORITHM, "typ": "JWT"}
            jwt_token = jwt.encode(payload, settings.JWT_AUTH.get('JWT_PRIVATE_KEY'), algorithm='RS256')
            return f"""{uuid_token}:{jwt_token}"""
        except Exception as e:
            raise e

    @classmethod
    def decrypt(cls, jwt_refresh_token: str):
        """
        To decrypt jwt token to the real refresh_token that was saved in our database

        :param jwt_refresh_token: the refresh_token after encrypted by jwt
        """
        parts = jwt_refresh_token.split(":")
        if len(parts) != 2:
            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, error='invalid JWT token')
        uid = parts[0]
        jwt_token = parts[1]
        auth_refresh_token = AuthRefreshTokenService.get_by_uuid_token(uuid=uid)
        if not auth_refresh_token:
            raise CustomException(error=ValidationErr.INVALID, params=[f"uuid_token ({uid})"])
        try:
            payload = jwt.decode(jwt_token, settings.JWT_AUTH.get('JWT_PUBLIC_KEY'), algorithms=[cls.JWT_ALGORITHM])
        except Exception:
            raise CustomException(error=ValidationErr.INVALID, field="jwt_token", params=["jwt_token"])
        return payload


class AuthJwtTokenService:
    @classmethod
    def validate_refresh_token(cls, request, refresh_token: str) -> bool:
        """
        Check refresh_token exists and refers to the right user.
        Also attach User instance to the request object
        """
        # null_or_recent = Q(revoked__isnull=True) | Q(revoked__gt=datetime.datetime.now())

        rt = AuthRefreshToken.objects.filter(revoked__isnull=True, token=refresh_token).first()
        if not rt:
            return False

        request.user = UserService.get_user(rt.user_id)
        request.refresh_token = rt.token
        request.refresh_token_instance = rt
        return True

    @classmethod
    def create_jwt_token(cls, request, **kwargs) -> Tuple[str, AuthRefreshToken, str]:
        """
        To create jwt Token
        :param request: The given request
        :param kwargs: Optional. The acceptance variables should be as format:
        {
            "skip_refresh_token": bool,
        }
        :return: access_token, refresh_token instance, encrypted_jwt_rf_token
        """

        skip_refresh_token = kwargs.get("skip_refresh_token", False)
        user = getattr(request, "user", None)
        if not user:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED, error=ValidationErr.DOES_NOT_EXIST, params=["User"]
            )

        access_token = ChromeExtensionJWTToken().encode_token(id=user.id, email=user.email, username=user.username, user_id=user.user_id)
        rt_instance = AuthRefreshToken(user=user)
        jwt_rf_token = ""
        if not skip_refresh_token:
            if hasattr(request, "refresh_token_instance"):
                request.refresh_token_instance.revoke()
            else:
                AuthRefreshToken.objects.filter(user_id=user.id).delete()
            refresh_token = Utils.id_generator(40)
            rt_instance.token = refresh_token
            rt_instance.save()
            jwt_rf_token = JWTRefreshTokenHelper.encrypt(refresh_token, user_id=user.id, email=user.email)

        return access_token, rt_instance, jwt_rf_token
