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


def create_question(title, content, username='testuser', due='2019-03-03T04:02:32.142923Z',
                    bounty=100, question_type='private'):
    client = Client()
    login(client)
    data = {
        'title': title,
        'content': content,
        'username': username,
        'due': due,
        'bounty': bounty,
        'question_type': question_type,
        'tags': ['tag1', 'tag2', 'tag3']
    }
    path = reverse('question_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


def create_information(title, content, username='testuser', hidden_exist=True, hidden_content='thisishidden',
                       due='2019-03-03T04:02:32.142923Z', hidden_content_cost=100, sponsor_credit=200):
    client = Client()
    login(client)

    data = {
        'title': title,
        'content': content,
        'username': username,
        'hidden_exist': hidden_exist,
        'hidden_content': hidden_content,
        'due': due,
        'hidden_content_cost': hidden_content_cost,
        'sponsor_credit': sponsor_credit,
        'tags': ['tag3', 'tag4', 'tag5']
    }

    path = reverse('information_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


class QuestionListTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')
        create_question(title='test title', content='test content')

    def test_get_list_question(self):
        client = Client()
        path = reverse('question_list')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_get_list_question_by_title(self):
        create_question(title='te2st title', content='test content')
        client = Client()
        path = reverse('question_list_by_title', kwargs={'title': 'test'})
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)


class InformationListTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')
        create_information(title='testtitle1', content='testcontent1')

    def test_get_information(self):
        client = Client()
        path = reverse('information_list')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_get_list_information_by_title(self):
        create_information(title='te2st title', content='test content')
        client = Client()
        path = reverse('information_list_by_title', kwargs={'title': 'test'})
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)


class TagListtests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')
        create_information(title='testtitle1', content='testcontent1')
        create_question(title='test title', content='test content')

    def test_get_taglist(self):
        client = Client()
        path = reverse('tag_list')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)
