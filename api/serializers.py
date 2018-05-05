from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('credit',)


class UserProfileSerializer(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def to_representation(self, instance):
        user = UserSerializer(instance)
        serialized_user = user.data
        profile = Profile.objects.get(instance)
        serialized_profile = ProfileSerializer(profile)

        serialized_user.pop('password')
        serialized_user.update(serialized_profile)

        return serialized_user
