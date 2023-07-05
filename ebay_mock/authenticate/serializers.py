from rest_framework import serializers


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=200)
    expires_in = serializers.IntegerField()
    token_type = serializers.CharField(max_length=200)
