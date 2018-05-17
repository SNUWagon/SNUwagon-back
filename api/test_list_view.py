import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User


class QuestionListTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample QuestionPost
        client = Client()

        data = {
            'title': 'testtitle11',
            'content': 'testcontent11',
            'username': 'testuser',
            'due': '2015-03-03T04:02:32.142923Z',
            'bounty': 100,
            'question_type': 'private'
        }

        path = reverse('question_posts')
        client.post(path=path,
                    data=json.dumps(data),
                    content_type='application/json')

    def test_get_list_question(self):
        client = Client()
        path = reverse('question_list')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)


class InformationListTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample InformationPost
        client = Client()

        data = {
            'title': 'testtitle11',
            'content': 'testcontent11',
            'username': 'testuser',
            'hidden_exist': True,
            'hidden_content': 'thisishidden!',
            'due': '2015-03-03T04:02:32.142923Z',
            'hidden_content_cost': 100,
            'sponsor_credit': 200
        }

        path = reverse('information_posts')
        client.post(path=path,
                    data=json.dumps(data),
                    content_type='application/json')

    def test_get_information(self):
        client = Client()
        path = reverse('information_list')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)
