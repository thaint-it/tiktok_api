
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.throttling import UserRateThrottle


class UserAccessRateThrottle(UserRateThrottle):
    def __init__(self):
        super().__init__()
        # self._is_premium_account = False

    # def _validate_request(self, request):
    #     user = request.user
        # self._is_premium_account = user and not isinstance(user, AnonymousUser) and user.account_type == AccountType.PREMIUM


class BaseUserThrottle(UserAccessRateThrottle):
    scope = "custom_user"
    # ASKING_ENDPOINT = "/api/v1/ai/ask_question"
    ident = ""

    def get_cache_key(self, request, view):
        ident = self.ident
        # if request.path == self.ASKING_ENDPOINT:
        #     ident = self.ident
        # else:
        #     ident = ""
        return self.cache_format % {"scope": self.scope, "ident": ident}

    def allow_request(self, request, view):
        # self._validate_request(request)
        # if self._is_premium_account:
        #     self.scope = "premium_user"

        # Prevent there are too many request have same params
        override_rate = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].get(self.scope)
        if override_rate:
            self.num_requests, self.duration = self.parse_rate(override_rate)
        apply_throttle = True
        # if request.method == "POST":
        #     self.ident = self.get_ident(request)
        #     apply_throttle = request.path == self.ASKING_ENDPOINT and self.ident
        if apply_throttle:
            return super().allow_request(request, view)
        else:
            return True
