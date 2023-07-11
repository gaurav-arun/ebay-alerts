import base64

from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions


class ClientCredentialsAuthentication(authentication.BaseAuthentication):
    def validate(self, body):
        #  Body is application/x-www-form-urlencoded with the following format:
        # 'grant_type=client_credentials&scope=api_scope1 api_scope2'
        body = body.decode("utf-8")
        if len(body.split("&")) != 2:
            raise exceptions.AuthenticationFailed("Invalid body")

        grant_type, scope = body.split("&")
        grant_type = grant_type.split("=")[1]
        scope = scope.split("=")[1]
        if grant_type != "client_credentials":
            raise exceptions.AuthenticationFailed("Invalid grant type")

        scopes = scope.split(" ")
        # Only `api_scope` is supported for now!
        if len(scopes) != 1:
            raise exceptions.AuthenticationFailed("Invalid scope")

        if not scopes[0].endswith("api_scope"):
            raise exceptions.AuthenticationFailed("Invalid scope")

    def authenticate(self, request):
        content_type = request.headers.get("Content-Type")
        if content_type != "application/x-www-form-urlencoded":
            raise exceptions.AuthenticationFailed("Invalid content type")

        content_type = request.headers.get("Authorization")
        auth_scheme, auth_credentials = content_type.split(" ")
        if auth_scheme.lower() != "basic":
            raise exceptions.AuthenticationFailed("Invalid authorization type")

        # `auth_credentials` is a base64 encoded string
        #  of the form '<client_id>:<client_secret>'
        auth_credentials = base64.b64decode(auth_credentials).decode("utf-8")
        if len(auth_credentials.split(":")) != 2:
            raise exceptions.AuthenticationFailed("Invalid authorization string")

        self.validate(request.body)

        return AnonymousUser(), None
