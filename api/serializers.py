from .models import Profile, QuestionPost, InformationPost, QuestionAnswer
from .models import Tag, BoughtInformation, Vote
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'credit',)


class UserProfileSerializer(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def to_representation(self, instance):
        user = UserSerializer(instance)
        serialized_user = user.data
        profile = Profile.objects.get(user=instance)
        serialized_profile = ProfileSerializer(profile).data

        serialized_user.pop('password')
        serialized_user.update(serialized_profile)

        return serialized_user


class QuestionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionPost
        fields = ('id', 'title', 'content', 'author', 'created', 'due', 'resolved',
                  'bounty', 'question_type', 'selected', 'tags')


class InformationPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationPost
        fields = ('id', 'title', 'content', 'author', 'hidden_exist', 'hidden_content',
                  'created', 'due', 'hidden_content_cost', 'sponsor_credit', 'tags')


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'content', 'author', 'created', 'question')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'tag_type', 'question', 'information')


class BoughtInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoughtInformation
        fields = ('user', 'post')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('vote_type', 'user', 'post', 'created', 'weight')
