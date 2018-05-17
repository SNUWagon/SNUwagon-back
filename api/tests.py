import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User


# put model tests here
class ModelTests(TestCase):

    # put default settings in here
    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

    def test_User_model(self):
        success = authenticate(username='testuser', password='userpassword')
        self.assertNotEqual(success, None)

        success = authenticate(username='testuser', password='NOTuserpassword')
        self.assertEqual(success, None)

    def test_Profile_model(self):
        user = User.objects.get(username='testuser')
        profile = Profile.objects.filter(user=user)

        self.assertNotEqual(len(profile), 0)
