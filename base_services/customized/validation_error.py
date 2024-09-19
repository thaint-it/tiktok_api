from django.utils.translation import gettext_lazy as _

class ValidationErr:
    REQUIRED = {"code": 1100, "message": _("{0} is required.")}
    NULL = {"code": 1101, "message": _("{0} may not be null.")}
    EMPTY = {"code": 1102, "message": _("{0} may not be empty.")}
    UNIQUE = {"code": 1103, "message": _("{0} must be unique.")}
    ALREADY_IN_USE = {"code": 1104, "message": _("{0} already in use.")}
    DOES_NOT_EXIST = {"code": 1105, "message": _("{0} does not exist.")}
    MAX_LENGTH = {"code": 1106, "message": _("{0} must be less than or equal to {1} characters.")}
    MIN_LENGTH = {"code": 1107, "message": _("{0} must be at least {1} characters.")}
    MAX_STRING_LENGTH = {"code": 1108, "message": _("String value too large.")}
    MAX_VALUE = {"code": 1109, "message": _("{0} must be less than or equal to {1}.")}
    MIN_VALUE = {"code": 1110, "message": _("{0} must be greater than or equal to {1}.")}
    MAX_DECIMAL_VALUE = {"code": 1111, "message": _("{0} is invalid.")}
    DATE = {"code": 1112, "message": _("{0} must be a date.")}
    DATETIME = {"code": 1113, "message": _("{0} must be a datetime.")}
    NOT_A_LIST = {"code": 1114, "message": _("{0} must be a list.")}
    NOT_A_DICT = {"code": 1115, "message": _("{0} must be a dict.")}
    INVALID = {"code": 1116, "message": _("{0} is invalid.")}
    INVALID_BOOLEAN = {"code": 1117, "message": _("{0} is not a valid boolean.")}
    INVALID_EMAIL = {"code": 1118, "message": _("{0} is not a valid email address.")}
    INVALID_REGEX = {"code": 1119, "message": _("{0} does not match the required pattern.")}
    INVALID_SLUG = {"code": 1120, "message": _("{0} is not a valid slug.")}
    INVALID_URL = {"code": 1121, "message": _("{0} is not a valid URL.")}
    INVALID_UUID = {"code": 1122, "message": _("{0} is not a valid UUID.")}
    INVALID_IP_ADDRESS = {"code": 1123, "message": _("{0} must be a valid IPv4 or IPv6 address.")}
    INVALID_INTEGER = {"code": 1124, "message": _("{0} is not a valid integer.")}
    INVALID_NUMBER = {"code": 1125, "message": _("{0} is not a valid number.")}
    INVALID_DATE = {"code": 1126, "message": _("{0} is not in date format.")}
    INVALID_TIME = {"code": 1127, "message": _("{0} is not in time format.")}
    INVALID_DATETIME = {"code": 1128, "message": _("{0} is not in datetime format.")}
    INVALID_DURATION = {"code": 1129, "message": _("{0} is not in duration format.")}
    INVALID_CHOICE = {"code": 1130, "message": _("{0} is not a valid choice.")}
    INVALID_FILE = {"code": 1131, "message": _("{0} is not a valid file.")}
    INVALID_FILE_PATH = {"code": 1132, "message": _("{0} is not a valid file path.")}
    INVALID_IMAGE = {"code": 1133, "message": _("{0} is not a valid image.")}
    INVALID_JSON = {"code": 1134, "message": _("{0} must be valid JSON.")}
    NO_FILE_NAME = {"code": 1135, "message": _("No filename could be determined.")}
    REQUIRED_FILE = {"code": 1136, "message": _("No file was submitted.")}
    EMPTY_FILE = {"code": 1137, "message": _("The submitted file is empty.")}
    EMPTY_LIST = {"code": 1138, "message": _("This list may not be empty.")}
    EMPTY_CHOICE = {"code": 1139, "message": _("This selection may not be empty.")}
    UNIQUE_SET = {"code": 1140, "message": _("The fields {0} must make a unique set.")}
    SET_PASSWORD_FAILED = {
        "code": 1141,
        "message": _("This is an old forgot password link. Please reset and try again."),
    }
    GENERAL = {"code": 1142, "message": "{0}"}

