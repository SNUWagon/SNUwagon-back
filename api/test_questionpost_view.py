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
        'question_type': question_type
    }
    path = reverse('question_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


def create_answer(qid, content, username='testuser'):
    client = Client()
    login(client)

    data = {
        'qid': qid,
        'content': content,
        'username': username,
    }
    path = reverse('question_answers')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


class QuestionPostTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')
        create_question(title='testtitle1', content='testcontent1')

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
        response = create_question(title='testtitle2', content='testcontent2')
        self.assertEqual(response.status_code, 201)
        response = create_question(title='testtitle3', content='testcontent3', bounty=1300)
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

    def test_answer(self):
        qid = get_any_valid_id()
        for i in range(3):
            response = create_answer(qid=qid, content='answertest')
            self.assertEqual(response.status_code, 201)

        # test if we can retrieve answers
        client = Client()
        login(client)
        path = reverse('question_answers')
        path = path + '/' + str(qid)
        response = client.get(path=path)
