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
    pass


class InformationPost(models.Model):
    pass


class QuestionAnswer(models.Model):
    pass


class Tag(models.Model):
    pass


class BoughtInformation(models.Model):
    pass


class Vote(models.Model):
    pass
