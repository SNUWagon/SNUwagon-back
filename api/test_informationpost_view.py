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
    every_informations = InformationPost.objects.all()
    information_id = 0
    for x in every_informations:
        information_id = x.id
    return information_id


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
        'sponsor_credit': sponsor_credit
    }

    path = reverse('information_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


class InformationPostTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample InformationPost
        create_information(title='testtitle1', content='testcontent1')

    def test_get_information(self):
        client = Client()
        login(client)

        information_id = get_any_valid_id()
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        # Make request and check reponse
        response = client.get(path=path)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_information(self):
        response = create_information(title='testtitle2', content='testcontent2')
        self.assertEqual(response.status_code, 201)

    def test_delete_information(self):
        client = Client()
        login(client)

        data = {}

        # Check for invalid delete
        path = reverse('information_posts')
        path = path + '/' + str(100)
        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        information_id = get_any_valid_id()
        # Check for valid delete
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
