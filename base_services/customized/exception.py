from rest_framework import exceptions, status
from typing import Any, Dict
from base_services.customized.api_error import ApiErr
from django.utils.translation import gettext_lazy as _

class CustomException(exceptions.ValidationError):
    """
        Base class for REST framework exceptions.
        Subclasses should provide `.status_code` and `.default_detail` properties.
        """

    status_code = 400
    error: Dict[str, Any] = {}
    field: str = ""

    def __init__(self, error={"code": 0, "message": ""}, params=[], field="", status_code=400):
        self.error = {}
        if error["code"] == ApiErr.SERVER_ERROR["code"]:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif error["code"] == ApiErr.PARSE_ERROR["code"]:
            status_code = status.HTTP_400_BAD_REQUEST
        elif error["code"] == ApiErr.AUTHENTICATION_FAILED["code"]:
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error["code"] == ApiErr.NOT_AUTHENTICATED["code"]:
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error["code"] == ApiErr.PERMISSION_DENIED["code"]:
            status_code = status.HTTP_403_FORBIDDEN
        elif error["code"] == ApiErr.NOT_FOUND["code"]:
            status_code = status.HTTP_404_NOT_FOUND
        elif error["code"] == ApiErr.METHOD_NOT_ALLOWED["code"]:
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        elif error["code"] == ApiErr.NOT_ACCEPTABLE["code"]:
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif error["code"] == ApiErr.CONFLICT["code"]:
            status_code = status.HTTP_409_CONFLICT
        elif error["code"] == ApiErr.UNSUPPORTED_MEDIA_TYPE["code"]:
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        elif error["code"] == ApiErr.THROTTLED["code"]:
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
        elif error["code"] == ApiErr.BAD_HEADER_PARAMS["code"]:
            status_code = status.HTTP_400_BAD_REQUEST
        elif error["code"] == ApiErr.TOKEN_EXPIRED["code"]:
            status_code = status.HTTP_400_BAD_REQUEST

        try:
            message = _(error["message"]).format(*params)
        except:
            message = _(error["message"])

        super().__init__({"code": error["code"], "message": message, "field": field})
        self.status_code = status_code
        self.error["code"] = error["code"]
        self.error["message"] = str(message)
        self.field = field

    def __str__(self):
        return self.error["message"]
