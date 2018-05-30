import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User


class DebugTests(TestCase):

    # put default settings in here
    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com',
                    verified=False)

    def test_debug_verify(self):
        client = Client()
        path = reverse('debug_verify', kwargs={'username': 'testuser'})
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_debug_credit(self):
        client = Client()
        path = reverse('debug_credit', kwargs={'username': 'testuser'})
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
