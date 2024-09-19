from users.models import AuthRefreshToken


class AuthRefreshTokenService:
    @classmethod
    def get_by_uuid_token(cls, uuid):
        return AuthRefreshToken.objects.filter(token=uuid, revoked__isnull=True)
