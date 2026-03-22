from .base import AppException
from fastapi import status

class SlugNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Slug is not found."

class SlugExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    message = "This link is already exists."
