from django.db import models
from django.db.utils import Error
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=100)
    created = models.DateTimeField(auto_created=True, auto_now=True)


# base create_user wrapper
def create_user(**kwargs):
    try:

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


class InformationPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Profile', related_name='informations_as_writer',
                               on_delete=models.CASCADE)
    hidden_exist = models.BooleanField()
    hidden_content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField()
    hidden_content_cost = models.IntegerField()
    sponsor_credit = models.IntegerField()


class QuestionAnswer(models.Model):
    content = models.TextField()
    author = models.ForeignKey('Profile', related_name='answers_as_writer',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('QuestionPost', related_name='answers',
                                 on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_type = models.CharField(max_length=100)
    question = models.ForeignKey('QuestionPost', related_name='tags',
                                 on_delete=models.SET_NULL, null=True)
    information = models.ForeignKey('InformationPost', related_name='tags',
                                    on_delete=models.SET_NULL, null=True)


class BoughtInformation(models.Model):
    user = models.ForeignKey('Profile', related_name='bought_informations',
                             on_delete=models.CASCADE)
    post = models.ForeignKey('InformationPost', related_name='buyers',
                             on_delete=models.CASCADE)
    cost = models.IntegerField()


class Vote(models.Model):
    vote_type = models.CharField(max_length=100)
    user = models.ForeignKey('Profile', related_name='votes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey('InformationPost', related_name='votes',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField()
