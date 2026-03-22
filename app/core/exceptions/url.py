from .base import AppException
from fastapi import status


class UrlIsTooLong(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    message = "URL is too long"
