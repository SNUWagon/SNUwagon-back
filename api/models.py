from django.db import models
from django.db.utils import Error
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from hashlib import md5


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=1000)
    created = models.DateTimeField(auto_created=True, auto_now=True)
    verified = models.BooleanField(default=False)
    hashstring = models.CharField(max_length=200, default='')


# base create_user wrapper
def create_user(**kwargs):
    try:
        if 'hashstring' not in kwargs:
            kwargs['hashstring'] = '!'
        if 'verified' not in kwargs:
            kwargs['verified'] = False
        if len(User.objects.filter(email=kwargs['email'])) > 0:
            return None

        user = User.objects.create_user(
            username=kwargs['username'],
            password=kwargs['password'],
            email=kwargs['email'],
            is_active=True,
        )

        new_user = Profile.objects.create(
            user=user,
            verified=kwargs['verified'],
            hashstring=kwargs['hashstring'],
        )

        return new_user

    except Error:
        return None


class QuestionPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Profile', related_name='questions_as_writer',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField()
    resolved = models.BooleanField(default=False)
    bounty = models.IntegerField()
    question_type = models.CharField(max_length=100)
    selected = models.ForeignKey('QuestionAnswer', related_name='selected_question',
                                 on_delete=models.SET_NULL, null=True)
    tags = ArrayField(models.CharField(max_length=64), blank=True, default=list)


class InformationPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Profile', related_name='informations_as_writer',
                               on_delete=models.CASCADE)
    hidden_exist = models.BooleanField(default=False)
    hidden_content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField()
    hidden_content_cost = models.IntegerField()
    sponsor_credit = models.IntegerField()
    tags = ArrayField(models.CharField(max_length=64), blank=True, default=list)


class QuestionAnswer(models.Model):
    content = models.TextField()
    author = models.ForeignKey('Profile', related_name='answers_as_writer',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('QuestionPost', related_name='answers',
                                 on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class BoughtInformation(models.Model):
    profile = models.ForeignKey('Profile', related_name='bought_informations',
                                on_delete=models.CASCADE)
    post = models.ForeignKey('InformationPost', related_name='buyers',
                             on_delete=models.CASCADE)


class Vote(models.Model):
    vote_type = models.CharField(max_length=100)
    profile = models.ForeignKey('Profile', related_name='votes',
                                on_delete=models.CASCADE)
    post = models.ForeignKey('InformationPost', related_name='votes',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField()


class Notification(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=200)
    content_id = models.IntegerField()
    message = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    pushed = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
