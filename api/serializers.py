from .models import Profile, QuestionPost, InformationPost, QuestionAnswer
from .models import Tag, BoughtInformation, Vote, Notification
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'credit', 'watch_tags')


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
        fields = ('profile', 'post')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('vote_type', 'post', 'created', 'voter', 'weight')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'profile', 'notification_type', 'content_id', 'message', 'created',
                  'pushed', 'read')
