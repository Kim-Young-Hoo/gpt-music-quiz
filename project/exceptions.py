from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class NotFoundEnumMember(Exception):
    def __init__(self, message="Enum member not found"):
        self.message = message
        super().__init__(self.message)


def global_exception_handler(exc, context):
    if isinstance(exc, NotFoundEnumMember):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    response = exception_handler(exc, context)
    return response
