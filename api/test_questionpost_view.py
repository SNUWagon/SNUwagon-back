import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User


def login(client):
    data = {
        'username': 'testuser',
        'password': 'userpassword'
    }

    path = reverse('sign_in')
    client.post(path=path,
                data=json.dumps(data),
                content_type='application/json')


def get_any_valid_id():
    # Choose any valid id
    every_questions = QuestionPost.objects.all()
    question_id = 0
    for x in every_questions:
        question_id = x.id
    return question_id


class QuestionPostTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample QuestionPost
        client = Client()
        login(client)

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

    def test_get_question(self):
        client = Client()
        login(client)

        question_id = get_any_valid_id()
        path = reverse('question_posts')
        path = path + '/' + str(question_id)

        # Make request and check reponse
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        client = Client()
        login(client)

        data = {
            'title': 'testtitle22',
            'content': 'testcontent22',
            'username': 'testuser',
            'due': '2015-03-03T04:02:32.142923Z',
            'bounty': 100,
            'question_type': 'private'
        }

        path = reverse('question_posts')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 201)

        # This is invalid request
        # Not enough credit
        data = {
            'title': 'testtitle22',
            'content': 'testcontent22',
            'username': 'testuser',
            'due': '2015-03-03T04:02:32.142923Z',
            'bounty': 300,
            'question_type': 'private'
        }

        path = reverse('question_posts')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_delete_question(self):
        client = Client()
        login(client)

        data = {}

        # Check for invalid delete
        path = reverse('question_posts')
        path = path + '/' + str(100)
        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Check for valid delete
        question_id = get_any_valid_id()
        path = reverse('question_posts')
        path = path + '/' + str(question_id)

        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
