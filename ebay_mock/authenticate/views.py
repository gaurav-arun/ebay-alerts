import secrets

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import ClientCredentialsAuthentication
from .serializers import AccessTokenSerializer


class ClientCredentials(APIView):
    """
    View to acquire an application access token.
    """

    authentication_classes = [ClientCredentialsAuthentication]

    def post(self, request, format=None):
        response = {
            "access_token": f"v^1.1#i^1#p^3#r^1#{secrets.token_urlsafe(32)}",
            "expires_in": 120,
            "token_type": "Application Access Token",
        }
        serializer = AccessTokenSerializer(data=response)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
