from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "email", "keywords", "frequency"]
