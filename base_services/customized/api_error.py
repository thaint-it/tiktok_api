
from django.utils.translation import gettext_lazy as _

class ApiErr:

    SERVER_ERROR = {"code": 1000, "message": _("A server error occurred.")}
    PARSE_ERROR = {"code": 1001, "message": _("Malformed request.")}
    AUTHENTICATION_FAILED = {"code": 1002, "message": _("Incorrect authentication credentials.")}
    NOT_AUTHENTICATED = {"code": 1003, "message": _("Authentication credentials were not provided.")}
    PERMISSION_DENIED = {"code": 1004, "message": _("You do not have permission to perform this action.")}
    NOT_FOUND = {"code": 1005, "message": _("{0} is not found.")}
    METHOD_NOT_ALLOWED = {"code": 1006, "message": _("Method not allowed.")}
    NOT_ACCEPTABLE = {"code": 1007, "message": _("Could not satisfy the request Accept header.")}
    UNSUPPORTED_MEDIA_TYPE = {"code": 1008, "message": _("Unsupported this media type in request.")}
    THROTTLED = {"code": 1009, "message": _("Request was throttled.")}
    BAD_HEADER_PARAMS = {"code": 1010, "message": _("Invalid request headers")}
    TOKEN_EXPIRED = {"code": 1011, "message": _("Token expired")}
    UNEXPECTED_ERROR = {"code": 1012, "message": "{0}"}
    CUSTOM_EXCEPTION = {"code": 1013, "message": "{0}"}
    BAD_REQUEST = {"code": 1014, "message": _("Bad request.")}
    INVALID_REQUEST = {"code": 1015, "message": _("Invalid request.")}
    CONFLICT = {"code": 1016, "message": _("{0} already exists")}
    DOES_NOT_SUPPORTED = {"code": 1018, "message": _("This API does not support yet")}

