import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user


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


# Api tests
#   - name api test 'Api(api_name)Tests

class ApiSignInTests(TestCase):

    # put default settings in here
    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

    def test_sign_in_success(self):
        client = Client()

        data = {
            'username': 'testuser',
            'password': 'userpassword',
        }

        path = reverse('sign_in')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_sign_in_fail(self):
        client = Client()

        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        path = reverse('sign_in')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 401)


class ApiSignUpTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

    def test_sign_up_success(self):
        client = Client()
        data = {
            'username': 'newtestuser',
            'password': 'newuserpassword',
            'email': 'newtest@test.com',
        }

        path = reverse('sign_up')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_sign_up_fail_by_duplicate_username(self):
        client = Client()

        data = {
            'username': 'testuser',
            'password': 'newuserpassword',
            'email': 'blabla@test.com',
        }

        path = reverse('sign_up')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_sign_up_fail_by_duplicate_email(self):
        client = Client()

        data = {
            'username': 'emailtestuser',
            'password': 'newuserpassword',
            'email': 'test@test.com',
        }

        path = reverse('sign_up')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 401)
