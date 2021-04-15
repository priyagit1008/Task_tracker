from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ParseError,
    ValidationError,
)

# logger
import logging
logger = logging.getLogger(__name__)




from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # check that a ValidationError exception is raised
    if isinstance(exc, ValidationError):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        if response.data.get("first_name", None):
            response.data = response.data["first_name"][0]
        elif response.data.get("email", None):
            response.data = response.data["email"][0]
        elif response.data.get("mobile", None):
            response.data = response.data["mobile"][0]

    return response


class ResourceConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Record already exists."

    def __init__(self, fields=None):
        if fields is not None:
            self.detail += " Duplicate Value for: %s" % (str(fields))


class NetworkException(APIException):
    pass


class ResourceNotFoundException(NotFound):
    pass


class ParseException(ParseError):
    def __init__(self, detail=None, code=None, errors=None):
        if errors:
            logger.info(errors)
        return super(ParseException, self).__init__(detail, code)


class BadRequestException(ValidationError):
    pass
