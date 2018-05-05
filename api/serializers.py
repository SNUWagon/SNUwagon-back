from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'credit')
