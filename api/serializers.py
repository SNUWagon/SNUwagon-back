from .models import User
from rest_framework import serializers


class UserSerializer(serializers.BaseSerializer):

    class Meta:
        model = User
        fields = ('user', 'credit')
