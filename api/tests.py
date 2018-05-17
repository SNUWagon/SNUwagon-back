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


class ApiSignOutTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

    def test_logout(self):
        client = Client()
        path = reverse('sign_out')
        response = client.get(path=path,
                              content_type='application/json')

        self.assertEqual(response.status_code, 200)


class ApiUserInfoTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

    def test_get_userinfo_success(self):
        client = Client()
        user = User.objects.get(username='testuser')
        userid = user.id

        path = reverse('user_info', kwargs={'id': userid})
        response = client.get(path=path,
                              content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json['data']['username'], 'testuser')

    def test_get_userinfo_fail(self):
        client = Client()

        path = reverse('user_info', kwargs={'id': 0})
        response = client.get(path=path,
                              content_type='application/json')

        self.assertEqual(response.status_code, 400)


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

        # Choose any valid id
        every_questions = QuestionPost.objects.all()
        question_id = 0
        for x in every_questions:
            question_id = x.id
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

        # Choose any valid id
        every_questions = QuestionPost.objects.all()
        question_id = 0
        for x in every_questions:
            question_id = x.id

        # Check for valid delete
        path = reverse('question_posts')
        path = path + '/' + str(question_id)

        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)


class InformationPostTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample InformationPost
        client = Client()
        login(client)

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
        login(client)

        # Choose any valid id
        every_informations = InformationPost.objects.all()
        information_id = 0
        for x in every_informations:
            information_id = x.id
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        # Make request and check reponse
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_create_information(self):
        client = Client()
        login(client)

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
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

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

        # Choose any valid id
        every_informations = InformationPost.objects.all()
        information_id = 0
        for x in every_informations:
            information_id = x.id

        # Check for valid delete
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)


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
