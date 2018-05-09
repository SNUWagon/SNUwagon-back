from .models import Profile, QuestionPost, InformationPost, QuestionAnswer
from .models import Tag, BoughtInformation, Vote
from django.contrib.auth.models import User
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


class QuestionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionPost
        fields = ('title', 'content', 'author', 'created', 'due', 'resolved',
                  'bounty', 'question_type', 'selected')


class InformationPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationPost
        fields = ('title', 'content', 'author', 'hidden_exist', 'hidden_content',
                  'created', 'due', 'hidden_content_cost', 'sponsor_credit')


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('content', 'author', 'created', 'question')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'tag_type', 'question', 'information')


class BoughtInformationSerializer(serializers.ModelSerializer):

    class Meta:
        models = BoughtInformation
        fields = ('user', 'post', 'cost')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        models = Vote
        fields = ('vote_type', 'user', 'post', 'created', 'weight')
